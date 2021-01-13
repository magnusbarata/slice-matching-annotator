from ipywidgets import Box, VBox, IntSlider, ToggleButtons, Label
import pydicom as dcm
import matplotlib.pyplot as plt

class SingleScan(VBox):
    def __init__(self, scandir, slider_range, answer, slices_per_scan=5):
        if answer:
            start_idx = int(answer.split('.')[0])
            layout = {'border': 'solid green'}
        else:
            start_idx = 1
            layout = {'border': 'solid red'}
        self.scandir = scandir
        self.date = scandir.split('/')[-1]
        self.slices_per_scan = slices_per_scan
        
        slider_label = Label(value=self.date)
        slider = IntSlider(
            min=1, max=slider_range-slices_per_scan+1,
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

        
    def _init_images(self, idx):
        self.ims = []
        plt.ioff()
        self.fig, axs = plt.subplots(1, 5)
        
        for i, ax in enumerate(axs):
            fname = f'{self.scandir}/{i+idx:08d}.DCM'
            self.ims.append(ax.imshow(dcm.dcmread(fname).pixel_array, cmap='gray'))
            ax.axis('off')
        
        plt.tight_layout(pad=0.1)
        self.fig.canvas.header_visible = False
        self.fig.canvas.footer_visible = False
        self.fig.canvas.toolbar_visible = False
    
    
    def _update_images(self, change):
        for i, im in enumerate(self.ims):
            fname = f'{self.scandir}/{change.new + i:08d}.DCM'
            im.set_data(dcm.dcmread(fname).pixel_array)
        self.fig.canvas.draw()
    
    
    def _create_btns(self, start_idx):
        btns = ToggleButtons(
            options=[i+start_idx for i in range(self.slices_per_scan)],
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