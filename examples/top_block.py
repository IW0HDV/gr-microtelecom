#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Thu Jan 29 15:58:41 2015
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import microtelecom
import sip
import sys

from distutils.version import StrictVersion
class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.wideband_bypass_ctr = wideband_bypass_ctr = 0
        self.samp_rate = samp_rate = 96000
        self.f_knob = f_knob = 7285000
        self.attenuator_ctr = attenuator_ctr = 0
        self.wide_band_bypass = wide_band_bypass = wideband_bypass_ctr
        self.freq = freq = f_knob
        self.firdes_tap = firdes_tap = firdes.low_pass(1,samp_rate,10000,4000,firdes.WIN_HAMMING, 6.76)
        self.att = att = attenuator_ctr

        ##################################################
        # Blocks
        ##################################################
        self._wideband_bypass_ctr_options = (0, 1, )
        self._wideband_bypass_ctr_labels = ("No bypass", "Wide Band", )
        self._wideband_bypass_ctr_tool_bar = Qt.QToolBar(self)
        self._wideband_bypass_ctr_tool_bar.addWidget(Qt.QLabel("wideband_bypass_ctr"+": "))
        self._wideband_bypass_ctr_combo_box = Qt.QComboBox()
        self._wideband_bypass_ctr_tool_bar.addWidget(self._wideband_bypass_ctr_combo_box)
        for label in self._wideband_bypass_ctr_labels: self._wideband_bypass_ctr_combo_box.addItem(label)
        self._wideband_bypass_ctr_callback = lambda i: Qt.QMetaObject.invokeMethod(self._wideband_bypass_ctr_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._wideband_bypass_ctr_options.index(i)))
        self._wideband_bypass_ctr_callback(self.wideband_bypass_ctr)
        self._wideband_bypass_ctr_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_wideband_bypass_ctr(self._wideband_bypass_ctr_options[i]))
        self.top_layout.addWidget(self._wideband_bypass_ctr_tool_bar)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_rate, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, -80)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, -80)
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.microtelecom_perseus_0 = microtelecom.perseus(samp_rate, freq, 0, 0, 0, wide_band_bypass)
          
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(4, (firdes_tap))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self._f_knob_layout = Qt.QVBoxLayout()
        self._f_knob_tool_bar = Qt.QToolBar(self)
        self._f_knob_layout.addWidget(self._f_knob_tool_bar)
        self._f_knob_tool_bar.addWidget(Qt.QLabel("Freq Hz"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._f_knob_counter = qwt_counter_pyslot()
        self._f_knob_counter.setRange(7100000, 7300000, 1000)
        self._f_knob_counter.setNumButtons(2)
        self._f_knob_counter.setValue(self.f_knob)
        self._f_knob_tool_bar.addWidget(self._f_knob_counter)
        self._f_knob_counter.valueChanged.connect(self.set_f_knob)
        self._f_knob_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._f_knob_slider.setRange(7100000, 7300000, 1000)
        self._f_knob_slider.setValue(self.f_knob)
        self._f_knob_slider.setMinimumWidth(200)
        self._f_knob_slider.valueChanged.connect(self.set_f_knob)
        self._f_knob_layout.addWidget(self._f_knob_slider)
        self.top_layout.addLayout(self._f_knob_layout)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((100, ))
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.audio_sink_0 = audio.sink(samp_rate/4, "", True)
        self._attenuator_ctr_options = (0, 10, 20, 30, )
        self._attenuator_ctr_labels = ("0dB", "-10dB", "-20dB", "-30dB", )
        self._attenuator_ctr_tool_bar = Qt.QToolBar(self)
        self._attenuator_ctr_tool_bar.addWidget(Qt.QLabel("ATT dB"+": "))
        self._attenuator_ctr_combo_box = Qt.QComboBox()
        self._attenuator_ctr_tool_bar.addWidget(self._attenuator_ctr_combo_box)
        for label in self._attenuator_ctr_labels: self._attenuator_ctr_combo_box.addItem(label)
        self._attenuator_ctr_callback = lambda i: Qt.QMetaObject.invokeMethod(self._attenuator_ctr_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._attenuator_ctr_options.index(i)))
        self._attenuator_ctr_callback(self.attenuator_ctr)
        self._attenuator_ctr_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_attenuator_ctr(self._attenuator_ctr_options[i]))
        self.top_layout.addWidget(self._attenuator_ctr_tool_bar)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.audio_sink_0, 0))
        self.connect((self.microtelecom_perseus_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_wideband_bypass_ctr(self):
        return self.wideband_bypass_ctr

    def set_wideband_bypass_ctr(self, wideband_bypass_ctr):
        self.wideband_bypass_ctr = wideband_bypass_ctr
        self.set_wide_band_bypass(self.wideband_bypass_ctr)
        self._wideband_bypass_ctr_callback(self.wideband_bypass_ctr)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_firdes_tap(firdes.low_pass(1,self.samp_rate,10000,4000,firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_f_knob(self):
        return self.f_knob

    def set_f_knob(self, f_knob):
        self.f_knob = f_knob
        self.set_freq(self.f_knob)
        Qt.QMetaObject.invokeMethod(self._f_knob_counter, "setValue", Qt.Q_ARG("double", self.f_knob))
        Qt.QMetaObject.invokeMethod(self._f_knob_slider, "setValue", Qt.Q_ARG("double", self.f_knob))

    def get_attenuator_ctr(self):
        return self.attenuator_ctr

    def set_attenuator_ctr(self, attenuator_ctr):
        self.attenuator_ctr = attenuator_ctr
        self.set_att(self.attenuator_ctr)
        self._attenuator_ctr_callback(self.attenuator_ctr)

    def get_wide_band_bypass(self):
        return self.wide_band_bypass

    def set_wide_band_bypass(self, wide_band_bypass):
        self.wide_band_bypass = wide_band_bypass
        self.microtelecom_perseus_0.set_wideband(self.wide_band_bypass)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.microtelecom_perseus_0.set_freq(self.freq)

    def get_firdes_tap(self):
        return self.firdes_tap

    def set_firdes_tap(self, firdes_tap):
        self.firdes_tap = firdes_tap
        self.fir_filter_xxx_0.set_taps((self.firdes_tap))

    def get_att(self):
        return self.att

    def set_att(self, att):
        self.att = att

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = top_block()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
