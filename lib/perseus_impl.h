/* -*- c++ -*- */
/* 
 * Copyright 2015 Andrea Montefusco IW0HDV.
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

#ifndef INCLUDED_MICROTELECOM_PERSEUS_IMPL_H
#define INCLUDED_MICROTELECOM_PERSEUS_IMPL_H


#include <boost/circular_buffer.hpp>
#include <boost/thread/mutex.hpp>
#include <boost/thread/condition.hpp>
#include <boost/timer/timer.hpp> // for auto_cpu_timer

#include <microtelecom/perseus.h>
#include <perseus-sdr.h>



namespace gr {
  namespace microtelecom {

    class perseus_impl : public perseus {
		
     public:
     
      perseus_impl(int sampling_rate=95000, int central_frequency=7070000, int attenuation_db= 0, bool adc_dither=0, bool preamp=0, bool frontend_filters=0);
      ~perseus_impl();

      // Where all the action really happens
      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
	       
       void  set_freq(float freq);
       void  set_attenuator(int attenuation_db); 
       void  set_dither(int adc_dither);
       void  set_preamp(int preamp);
       void  set_wideband(int frontend_filters);
       
     private:

      perseus_descr *pd; // pointer to libperseus-sdr descriptor
      bool d_started;    // flags that Perseus is enabled and running

      // vars to keep memory hardware status
      int            d_sampling_rate;
      int            d_central_frequency;
      int            d_attenuation_db;
      bool           d_adc_dither;
      bool           d_preamp;
      bool           d_frontend_filters;

      // hardware data
      unsigned short d_serial_number; // product id
      char           d_signature[16]; // product signature "0000-0000-0000"
      unsigned short d_hw_release;    // hardware release
      unsigned short d_hw_version;    // hardware version
      
      // ring buffer
      boost::circular_buffer<gr_complex> *_fifo;
      boost::mutex _fifo_lock;
      boost::condition_variable _samp_avail;
      
      static int callbackPerseus (void *buf, int buf_size, void *extra);
      
      // utility for exception throw
      void bail(const char *msg);
      
    };

  } // namespace microtelecom
} // namespace gr

#endif /* INCLUDED_MICROTELECOM_PERSEUS_IMPL_H */

