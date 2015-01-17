/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
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


#ifndef INCLUDED_MICROTELECOM_PERSEUS_H
#define INCLUDED_MICROTELECOM_PERSEUS_H

#include <microtelecom/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace microtelecom {

    /*!
     * \brief Perseus Receiver source block
     * \ingroup microtelecom
     *
     */
    class MICROTELECOM_API perseus : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<perseus> sptr;

      /*! \brief Set frequency with Hz resolution.
       *  \param freq The frequency in Hz
       *
       * Set the frequency of the Perseus receiver
       */
      virtual void  set_freq(float freq)               = 0;
      virtual void  set_attenuator(int attenuation_db) = 0;
      virtual void  set_dither(int adc_dither)         = 0;
      virtual void  set_preamp(int preamp)             = 0;
      virtual void  set_wideband(int frontend_filters) = 0;


      /*!
       * \brief Return a shared_ptr to a new instance of microtelecom::perseus.
       *
       * To avoid accidental use of raw pointers, microtelecom::perseus's
       * constructor is in a private implementation
       * class. microtelecom::perseus::make is the public interface for
       * creating new instances.
       */
//      static sptr make(int sampling_rate = 95000, int central_frequency = 7070000, int attenuation_db = 0, bool adc_dither = 0, bool preamp = 0, bool frontend_filters = 0)
      static sptr make(int sampling_rate, int central_frequency, int attenuation_db, bool adc_dither, bool preamp, bool frontend_filters)
                  throw (std::runtime_error) ;
    };

  } // namespace microtelecom
} // namespace gr

#endif /* INCLUDED_MICROTELECOM_PERSEUS_H */

