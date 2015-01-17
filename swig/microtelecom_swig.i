/* -*- c++ -*- */

#define MICROTELECOM_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "microtelecom_swig_doc.i"

%{
#include "microtelecom/perseus.h"
%}


%include "microtelecom/perseus.h"
GR_SWIG_BLOCK_MAGIC2(microtelecom, perseus);
