#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

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
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import microtelecom
import sip
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
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
        self.wideband_bypass_ctr = wideband_bypass_ctr = True
        self.samp_rate = samp_rate = 96000
        self.f_knob = f_knob = 7075000
        self.attenuator_ctr = attenuator_ctr = 0
        self.wide_band_bypass = wide_band_bypass = wideband_bypass_ctr
        self.freq = freq = f_knob
        self.firdes_tap = firdes_tap = firdes.low_pass(1,samp_rate,4000,1000,firdes.WIN_HAMMING, 6.76)
        self.att = att = attenuator_ctr

        ##################################################
        # Blocks
        ##################################################
        _wideband_bypass_ctr_check_box = Qt.QCheckBox('Wideband bypass control')
        self._wideband_bypass_ctr_choices = {True: True, False: False}
        self._wideband_bypass_ctr_choices_inv = dict((v,k) for k,v in self._wideband_bypass_ctr_choices.iteritems())
        self._wideband_bypass_ctr_callback = lambda i: Qt.QMetaObject.invokeMethod(_wideband_bypass_ctr_check_box, "setChecked", Qt.Q_ARG("bool", self._wideband_bypass_ctr_choices_inv[i]))
        self._wideband_bypass_ctr_callback(self.wideband_bypass_ctr)
        _wideband_bypass_ctr_check_box.stateChanged.connect(lambda i: self.set_wideband_bypass_ctr(self._wideband_bypass_ctr_choices[bool(i)]))
        self.top_grid_layout.addWidget(_wideband_bypass_ctr_check_box)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_rate, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
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
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
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
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.microtelecom_perseus_0 = microtelecom.perseus(samp_rate, freq, att, False, False, wide_band_bypass)

        self.fir_filter_xxx_0 = filter.fir_filter_ccc(2, (firdes_tap))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self._f_knob_range = Range(7000000, 7300000, 100, 7075000, 200)
        self._f_knob_win = RangeWidget(self._f_knob_range, self.set_f_knob, 'Freq Hz', "counter_slider", float)
        self.top_grid_layout.addWidget(self._f_knob_win)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((2000, ))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.audio_sink_0 = audio.sink(samp_rate/2, 'pulse', True)
        self._attenuator_ctr_options = (0, 10, 20, 30, )
        self._attenuator_ctr_labels = ('0dB', '-10dB', '-20dB', '-30dB', )
        self._attenuator_ctr_tool_bar = Qt.QToolBar(self)
        self._attenuator_ctr_tool_bar.addWidget(Qt.QLabel('ATT dB'+": "))
        self._attenuator_ctr_combo_box = Qt.QComboBox()
        self._attenuator_ctr_tool_bar.addWidget(self._attenuator_ctr_combo_box)
        for label in self._attenuator_ctr_labels: self._attenuator_ctr_combo_box.addItem(label)
        self._attenuator_ctr_callback = lambda i: Qt.QMetaObject.invokeMethod(self._attenuator_ctr_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._attenuator_ctr_options.index(i)))
        self._attenuator_ctr_callback(self.attenuator_ctr)
        self._attenuator_ctr_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_attenuator_ctr(self._attenuator_ctr_options[i]))
        self.top_grid_layout.addWidget(self._attenuator_ctr_tool_bar)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_real_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.microtelecom_perseus_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.microtelecom_perseus_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.microtelecom_perseus_0, 0), (self.qtgui_waterfall_sink_x_0, 0))

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
        self.set_firdes_tap(firdes.low_pass(1,self.samp_rate,4000,1000,firdes.WIN_HAMMING, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_f_knob(self):
        return self.f_knob

    def set_f_knob(self, f_knob):
        self.f_knob = f_knob
        self.set_freq(self.f_knob)

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
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
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
        self.microtelecom_perseus_0.set_attenuator(self.att)


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
