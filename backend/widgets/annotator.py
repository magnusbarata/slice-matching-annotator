import os
import json
import matplotlib.pyplot as plt
from ipywidgets import Box, VBox, Dropdown, Button
from .single_scan import SingleScan

class Annotator(VBox):
    def __init__(self, data_dir, out_name='GT', slices_per_scan=5):
        self.data_dir = data_dir
        self.out_name = f'annotated/{out_name}.json'
        self.slices_per_scan = slices_per_scan
        self.patients = [d.name for d in os.scandir(data_dir) if d.is_dir()]
        self._load_answer()

        self.patient_selector = Dropdown(
            options=self.patients,
            description='患者選択:',
            value=None
        )
        save_button = Button(description='回答を保存して次へ')
        self.scans_grid = VBox()
        
        self.patient_selector.observe(self._update_scan_grids, 'value')
        save_button.on_click(self._save_btn_clk)
        super().__init__([Box([self.patient_selector, save_button]), self.scans_grid])

    
    def _load_answer(self):
        try:
            with open(self.out_name, 'r') as fp:
                self.answer = json.load(fp)
        except FileNotFoundError:
            self.answer = {p: {} for p in self.patients}
        

    def _update_scan_grids(self, change):
        plt.close('all')
        pdir = f'{self.data_dir}/{change.new}'
        children = []
        for scan in os.scandir(pdir):
            if not scan.is_dir(): continue
            scandir = f'{pdir}/{scan.name}'
            files = [f for f in os.listdir(scandir) if f.endswith('.DCM')]
            scan_widget = SingleScan(
                scandir=scandir,
                slider_range=len(files),
                slices_per_scan=self.slices_per_scan,
                answer=self.answer[change.new].get(scan.name, '未回答')
            )
            children.append(scan_widget)
        self.scans_grid.children = children
    
    
    def _save_btn_clk(self, btn):
        ans_dict = {scan.date: scan.ans for scan in self.scans_grid.children}
        self.answer[self.patient_selector.value] = ans_dict
        with open(self.out_name, 'w') as fp:
            json.dump(self.answer, fp)
        self._get_next_patient()
    

    def _get_next_patient(self):
        next_idx = self.patients.index(self.patient_selector.value) + 1
        self.patient_selector.value = self.patients[next_idx % len(self.patients)]