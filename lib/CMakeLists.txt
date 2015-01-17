# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})

list(APPEND microtelecom_sources
    perseus_impl.cc
)

set(microtelecom_sources "${microtelecom_sources}" PARENT_SCOPE)
if(NOT microtelecom_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT microtelecom_sources)

add_library(gnuradio-microtelecom SHARED ${microtelecom_sources})
target_link_libraries(gnuradio-microtelecom ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES} ${PERSEUS_LIBRARIES})
set_target_properties(gnuradio-microtelecom PROPERTIES DEFINE_SYMBOL "gnuradio_microtelecom_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-microtelecom PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
install(TARGETS gnuradio-microtelecom
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_microtelecom_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_microtelecom.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_microtelecom.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_perseus.cc
)

add_executable(test-microtelecom ${test_microtelecom_sources})

target_link_libraries(
  test-microtelecom
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  ${PERSEUS_LIBRARIES}
  gnuradio-microtelecom
)

include_directories(${PERSEUS_INCLUDE_DIRS})

GR_ADD_TEST(test_microtelecom test-microtelecom)
