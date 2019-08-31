/* -*- c++ -*- */
/* 
 * Copyright 2015  Andrea Montefusco IW0HDV
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif


#include <gnuradio/io_signature.h>
#include "perseus_impl.h"

namespace gr {
  namespace microtelecom {

    perseus::sptr
    perseus::make(int sampling_rate, int central_frequency, int attenuation_db, bool adc_dither, bool preamp, bool frontend_filters)
    {
        int num_perseus = perseus_init();
    
        if (num_perseus > 0){
    	    printf("%d Perseus receivers found\n",num_perseus);
    	    // debug for libperseus-sdr library (look to stderror messages starting with: "perseus")
            perseus_set_debug(9); 
        } else {
            printf("Perseus hardware not found: %s\n",perseus_errorstr());
            throw std::runtime_error("perseus hw not found");
        }
        return gnuradio::get_initial_sptr
               (new perseus_impl(sampling_rate, central_frequency, attenuation_db, adc_dither, preamp, frontend_filters));
    }



    void  perseus_impl::set_freq (float freq)
    {
        printf("Setting Center frequency: %f\n", freq);
        perseus_set_ddc_center_freq(pd,double(d_central_frequency=(int)freq),d_frontend_filters);
    }

    void  perseus_impl::set_attenuator(int attenuation_db)
    {
        printf("Setting Attenuator: %d dB\n", attenuation_db);
        if(perseus_set_attenuator_in_db(pd,d_attenuation_db=attenuation_db)<0) {
            bail("Attenuator error");
        }
    }

    void  perseus_impl::set_dither(int adc_dither)
    {
        printf("Setting ADC: %d\n", adc_dither);
        if(perseus_set_adc(pd, d_adc_dither=adc_dither, d_preamp)<0) {
            bail("ADC dither setting error");
        }
    }
    
    void  perseus_impl::set_preamp(int preamp)
    {        
        printf("Setting Preamplifier: %d\n", preamp);
        if(perseus_set_adc(pd, d_adc_dither, d_preamp=preamp)<0) {
            bail("Preamplifier setting error");
        }
    }

    void  perseus_impl::set_wideband(int frontend_filters)
    {
        printf("Setting Wideband bypass: %d\n", frontend_filters);
        if(perseus_set_ddc_center_freq(pd,d_central_frequency,d_frontend_filters=frontend_filters)<0) {
            bail("Wideband bypass setting error");
        }
    }



    /*
     * The private constructor
     */
    perseus_impl::perseus_impl(int sampling_rate, int central_frequency, int attenuation_db, bool adc_dither, bool preamp, bool frontend_filters):
        gr::sync_block("perseus",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1 /*<+MIN_OUT+>*/, 1 /*<+MAX_OUT+>*/, sizeof(gr_complex)) ),

        pd(0),
        d_started(0),
        d_sampling_rate(sampling_rate),
        d_central_frequency(central_frequency),
        d_attenuation_db(attenuation_db),
        d_adc_dither(adc_dither),
        d_preamp(preamp),
        d_frontend_filters(frontend_filters)
    {
        // create the fifo 
        _fifo = new boost::circular_buffer<gr_complex>(5000000);
        if (!_fifo) 
           throw std::runtime_error( std::string(__FUNCTION__) 
                                     + " " 
                                     + "Failed to allocate a sample FIFO!" );

        // Open the first one...
        if ((pd = perseus_open(0))==NULL) bail("perseus_open error !");
        
        // Download the Cypress FX-2 microcontroller firmware to the unit
        // This is really done only the first time after a cold reset
        // The libperseus-sdr is now able to do that looking to USB endpoints
        // exported from the unit
        printf ("Downloading firmware...\n");
        if (perseus_firmware_download (pd,NULL)<0) 
            bail ("Perseus firmware download error !");
        
        // Sampling Rate, Configuring FPGA
        printf("Configuring FPGA...(%d)\n", d_sampling_rate);
        if(perseus_set_sampling_rate(pd,d_sampling_rate)<0)
            bail("perseus FPGA configuration error");

        // Save some information about the receiver (S/N and HW rev)
        eeprom_prodid prodid; // Perseus library data structure
        if (perseus_is_preserie(pd, 0) >= 0)
            printf("The device is a preserie unit");
        else
            if (perseus_get_product_id (pd,&prodid) >= 0) {
               snprintf(d_signature, sizeof(d_signature), 
                        "%02hX%02hX-%02hX%02hX-%02hX%02hX",
                        (uint16_t) prodid.signature[5],
                        (uint16_t) prodid.signature[4],
                        (uint16_t) prodid.signature[3],
                        (uint16_t) prodid.signature[2],
                        (uint16_t) prodid.signature[1],
                        (uint16_t) prodid.signature[0]
               );
               d_serial_number = (uint16_t) prodid.sn;
               d_hw_release = (uint16_t) prodid.hwrel;
               d_hw_version = (uint16_t) prodid.hwver;
            } else {
               printf("get product id error: %s", perseus_errorstr());
            }

        // Disable ADC Dither, Disable ADC Preamp
        perseus_set_adc (pd, false, false);
            
        // Set preselection filters (WB_MODE) and NCO frequency 
        perseus_set_ddc_center_freq (pd, d_central_frequency, 1);
        
        // Set the attenuator
        perseus_set_attenuator(pd, PERSEUS_ATT_0DB);
        
        // Centre frequency
        printf("Setting Center frequency: %d\n", d_central_frequency);
        perseus_set_ddc_center_freq(pd, double(d_central_frequency), d_frontend_filters);

        // start the reception loop
        int bs = 6144*2;
        if(perseus_start_async_input(pd,bs,callbackPerseus,(void*)this)<0) {
            bail("Error in async input");
        } else {
            printf("Async input STARTED (BUFFER SIZE: %d)\n", bs);
            d_started = 1;
        }
    }

    /*
     * Our virtual destructor.
     */
    perseus_impl::~perseus_impl() 
    {	
        printf("ModPerseusSource_impl::~ModPerseusSource_imp\n");
        if (d_started) {
            perseus_stop_async_input(pd);
            d_started = 0;
        }
        perseus_close(pd);
        perseus_exit();

        // free fifo object
        if (_fifo) {
           delete _fifo;
           _fifo = 0;
        }        
    }


    //
    // Code taken from OSMOCOM Gnu Radio module
    //
    int
    perseus_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        gr_complex *out = (gr_complex *) output_items[0];

        if ( !d_started )
           return WORK_DONE;

        boost::unique_lock<boost::mutex> lock(_fifo_lock);

        /* Wait until we have the requested number of samples */
        int n_samples_avail = _fifo->size();

        while (n_samples_avail < noutput_items) {
           _samp_avail.wait(lock);
           n_samples_avail = _fifo->size();
        }

        for(int i = 0; i < noutput_items; ++i) {
           out[i] = _fifo->at(0);
           _fifo->pop_front();
        }

        //std::cerr << "-" << std::flu
        // Tell runtime system how many output items we produced.
        return noutput_items;
    }
    
    

    int perseus_impl::callbackPerseus(void *buf, int buf_size, void *param)
    {
        const float NORM_FACTOR = static_cast<float> (static_cast<double> (1L<<31) );
        typedef union {
            struct __attribute__((__packed__)) {
                int32_t i;
                int32_t q;
            } iq; 
            struct __attribute__((__packed__)) {
                uint8_t i1;
                uint8_t i2;
                uint8_t i3;
                uint8_t i4;
                uint8_t q1;
                uint8_t q2;
                uint8_t q3;
                uint8_t q4;
            };
        } iq_sample;

        uint8_t *samplebuf        = (uint8_t*)buf;
        int nIQValues             = buf_size/6;

        perseus_impl *self  = (perseus_impl *)param;
        if(self == 0) {
            printf ("perseus_impl::callbackPerseus: FATAL: self == 0\n");
            return 0;
        }

        // samples received
        int num_samples = nIQValues;

        // compute space on fifo and how many samples can be copied
        size_t n_avail = self->_fifo->capacity() - self->_fifo->size();
        size_t to_copy = (n_avail < num_samples ? n_avail : num_samples);

        self->_fifo_lock.lock();

        for (int i = 0; i < to_copy; i++ ) {
            iq_sample s;

            s.i1 = 0;
            s.i2 = *samplebuf++;
            s.i3 = *samplebuf++;
            s.i4 = *samplebuf++;
            s.q1 = 0;
            s.q2 = *samplebuf++;
            s.q3 = *samplebuf++;
            s.q4 = *samplebuf++;
            
            self->_fifo->push_back( gr_complex( (((float)s.iq.i/NORM_FACTOR)), (((float)s.iq.q/NORM_FACTOR)) ) );
        }
        self->_fifo_lock.unlock();


        /* We have made some new samples available to the consumer in work() */
        if (to_copy) /* std::cerr << "+" << std::flush, */ self->_samp_avail.notify_one();

        /* Indicate overrun, if necessary */
        if (to_copy < num_samples) std::cerr << "O" << std::flush;

        return 0;
    }
    
    void perseus_impl::bail(const char *msg) 
    {
        fprintf(stderr,"FATAL: %s: %s",msg,perseus_errorstr());
        throw std::runtime_error("perseus");
    }
        

  } /* namespace microtelecom */
} /* namespace gr */

