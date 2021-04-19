import os
import json
import matplotlib.pyplot as plt
import pydicom as dcm
import numpy as np
from ipywidgets import Box, VBox, Dropdown, Button, Output

class Checker(VBox):
    def __init__(self, data_root, fname='GT'):
        self.data_root = data_root
        self.answer = self._load_answer(f'annotated/{fname}.json')
        self.patients = [k for k, v in self.answer.items() if v]
        
        self.patient_selector = Dropdown(
            options=self.patients,
            description='患者選択:'
        )
        next_btn = Button(description='次へ')
        prev_btn = Button(description='前へ')
        self.canvas = Output()

        self.patient_selector.observe(self._update_display, 'value')
        next_btn.on_click(self._change_patient)
        prev_btn.on_click(self._change_patient)
        if self.patients:
            super().__init__([Box([prev_btn, self.patient_selector, next_btn]), self.canvas])
            self._update_display()
        else:
            super().__init__()


    def _load_answer(self, fname):
        try:
            with open(fname, 'r') as fp:
                return json.load(fp)
        except FileNotFoundError:
            print('File not found')
            return {}


    def _change_patient(self, btn):
        next_idx = self.patients.index(self.patient_selector.value)
        next_idx +=  1 if btn.description == '次へ' else -1
        self.patient_selector.value = self.patients[next_idx % len(self.patients)]


    def _update_display(self, change=None):
        plt.close('all')
        plt.ioff()
        plt.tight_layout(pad=0.1)

        patient = change.new if change else self.patients[0]
        fig, axs = plt.subplots(1, len(self.answer[patient]))
        for i, (scan, slc) in enumerate(self.answer[patient].items()):
            fname = f'{self.data_root}/{patient}/{scan}/{slc}'
            axs[i].imshow(self._load_image(fname), cmap='gray')
            axs[i].set_title(scan, fontdict={'fontsize': 5})
            axs[i].axis('off')
        
        fig.canvas.header_visible = False
        fig.canvas.footer_visible = False
        fig.canvas.toolbar_visible = False
        with self.canvas:
            self.canvas.clear_output()
            fig.show()


    def _load_image(self, fname, WC=None, WW=None):
        try:
            ds = dcm.dcmread(fname)
            WC = WC if WC else ds.WindowCenter
            WW = WW if WW else ds.WindowWidth
            if type(WW) is dcm.multival.MultiValue:
                WW = WW[0]
            if type(WC) is dcm.multival.MultiValue:
                WC = WC[0]
            img_min = WC - WW // 2
            img_max = WC + WW // 2
            img = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept 
            img[img < img_min] = img_min
            img[img > img_max] = img_max
            return img
        except FileNotFoundError:
            return np.ones((512, 512, 3), dtype='float')