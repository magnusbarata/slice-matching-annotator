from ipywidgets import Box, VBox, IntSlider, ToggleButtons, Label
import pydicom as dcm
import numpy as np
import matplotlib.pyplot as plt

class SingleScan(VBox):
    def __init__(self, scandir, n_files, answer, slices_per_scan=5):
        if answer:
            start_idx = int(answer.split('.')[0])
            layout = {'border': 'solid green'}
        else:
            start_idx = 1
            layout = {'border': 'solid red'}
        self.scandir = scandir
        self.n_files = n_files
        self.date = scandir.split('/')[-1]
        self.slices_per_scan = slices_per_scan
        
        slider_label = Label(value=self.date)
        slider = IntSlider(
            min=1, max=n_files,
            value=start_idx,
            continous_updates=False
        )
        self.buttons = Box([self._create_btns(start_idx)])
        self.answer = Label(value=answer if answer else '未回答')
        self._init_images(start_idx)
        
        slider.observe(self._update_images, 'value')
        slider.observe(self._update_buttons, 'value')
        super().__init__([Box([slider_label, slider, self.answer]),
                          self.fig.canvas, self.buttons], layout=layout)

    
    def _load_image(self, fname, WC=None, WW=None):
        ds = dcm.dcmread(fname)
        WC = WC if WC else ds.WindowCenter
        WW = WW if WW else ds.WindowWidth
        img_min = WC - WW // 2
        img_max = WC + WW // 2
        img = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept 
        img[img < img_min] = img_min
        img[img > img_max] = img_max
        return img


    def _load_images(self, start_idx):
        for i, ax in enumerate(self.axs):
            if start_idx + i > self.n_files:
                ax.imshow(np.ones((512, 512, 3), dtype='float'))
            else:
                fname = f'{self.scandir}/{start_idx + i:08d}.DCM'
                ax.imshow(self._load_image(fname), cmap='gray')
            ax.axis('off')


    def _init_images(self, start_idx):
        plt.ioff()
        self.fig, self.axs = plt.subplots(1, 5)
        self._load_images(start_idx)
        plt.tight_layout(pad=0.1)
        self.fig.canvas.header_visible = False
        self.fig.canvas.footer_visible = False
        self.fig.canvas.toolbar_visible = False
    
    
    def _update_images(self, change):
        self._load_images(change.new)
        self.fig.canvas.draw()
    
    
    def _create_btns(self, start_idx):
        opt_max = min(start_idx + self.slices_per_scan, self.n_files + 1)
        btns = ToggleButtons(
            options=[i for i in range(start_idx, opt_max)],
            value=None,
            style={'button_width': '120px'}
        )
        btns.observe(self._select_slice, 'value')
        return btns


    def _update_buttons(self, change):
        self.buttons.children = [self._create_btns(change.new)]


    def _select_slice(self, change):
        self.layout = {'border': 'solid green'}
        self.answer.value = f'{change.new:08d}.DCM'
        
    
    @property
    def ans(self):
        if self.answer.value == '未回答':
            return None
        else:
            return self.answer.value