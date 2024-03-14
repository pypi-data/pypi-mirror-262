#! /usr/bin/env python3
import os
import sys
import threading
import time
from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
                             QFileDialog, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QMainWindow, QPushButton, QTextBrowser,
                             QTextEdit, QVBoxLayout, QWidget)

from SimpliPyTEM.App_functions import video_processing, isvideo, frames_processing, get_files_from_pattern
from SimpliPyTEM.html_writer import write_html, write_css, get_files_html
from SimpliPyTEM.PDF_generator import pdf_generator
from SimpliPyTEM.Micrograph_class import default_image_pipeline

class MainApplication(QWidget):
    def __init__(self):
        super().__init__()
        # Qt.AlignHCenter

        self.setGeometry(500, 500, 100, 400)
        self.setWindowTitle("SimpliPyTEM-GUI")

        self.title = QLabel("SimpliPyTEM-GUI", self)
        self.title.setObjectName("title")
        # app.setStyleSheet("QLabel, QCheckBox{font-size: 16pt;}")

        self.folderlabel = QLabel(
            "Process a folder, a file or \nliveprocessing a folder:"
        )
        # label.setLayout(layout)
        # self.label2 = QLabel('Choose whether to process a file, a folder, or live during an imaging session',self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Live
        self.live = "Folder"
        self.live_choice = QComboBox(self)
        # live_button.clicked.connect(self.liveCommand)
        choices = ["Folder", "File", "Live Processing"]
        self.folder_option = choices[0]
        self.live_choice.addItems(["Folder", "File", "Live Processing"])
        self.live_choice.currentTextChanged.connect(self.text_changed)
        # live_choice.setLayout(layout)

        self.folderpath = None
        self.folderpath_label = QLabel("")

        # For giving an input pattern
        self.filepattern_label = QLabel(
            "Input File Pattern\ne.g. *.tif means all .tif files (default= *.dm*)\n"
        )
        self.filepattern_box = QLineEdit(self)
        
        #Contrast enhance check box
        self.contrast_check = QCheckBox('Enhance Contrast', self)
        self.contrast_check.toggled.connect(self.update_contrast)
        self.contrast_state = True
        self.contrast_check.setChecked(True)

        # Checkbox for median filter
        self.med_check = QCheckBox("Median filter", self)
        # self.med_check.setEnabled(True)
        self.med_check.toggled.connect(self.updateMed)
        self.Med_state = True
        self.med_check.setChecked(True)
        # Value choicec for median filter
        self.med_filter_value = 3
        self.med_choice = QComboBox(self)
        self.med_choice.addItems(["3", "5", "7", "9", "11"])
        self.med_choice.currentTextChanged.connect(self.med_int_changed)

        # Checkbox for gaussian filter
        self.gauss_check = QCheckBox("Gaussian Filter", self)
        self.gauss_check.toggled.connect(self.updateGauss)
        self.gauss_check.setChecked(False)
        self.Gauss_state = False

        # value for gaussian filter
        self.gauss_filter_value = 3
        self.gauss_choice = QComboBox(self)
        self.gauss_choice.addItems(["3", "5", "7", "9", "11"])
        self.gauss_choice.currentTextChanged.connect(self.gauss_int_changed)

        # Checkbox for bin
        self.bin_check = QCheckBox("Bin image", self)
        self.bin_check.toggled.connect(self.updateBin)
        self.bin_check.setChecked(True)
        self.Bin_state = True

        # Value for bin
        self.bin_value = 2
        self.bin_choice = QComboBox(self)
        self.bin_choice.addItems(["2", "4", "8"])
        self.bin_choice.currentTextChanged.connect(self.gauss_int_changed)

        # Checkbox for scalebar
        self.scalebar_on = True
        self.scalebar_check = QCheckBox("Scalebar", self)
        self.scalebar_check.toggled.connect(self.updateScalebar)
        self.scalebar_check.setChecked(True)

        self.output_type_label = QLabel(
            'Choose image output type:'
        )
        # combo box for output image type
        self.output_type = 'jpg'
        self.output_choice = QComboBox(self)
        self.output_choice.addItems(['jpg', 'tif 8-bit', 'tif 32-bit'])
        self.output_choice.currentTextChanged.connect(self.output_choice_changed)

        # Checkbox for topaz_denoise and using cuda GPU

        self.topaz_label = QLabel(
            "Use Topaz Denoising? (requires setup, see docs for details) "
        )

        self.topaz_on = False
        self.topaz_check = QCheckBox("Denoise using Topaz", self)
        self.topaz_check.toggled.connect(self.updateTopaz)
        self.topaz_check.setChecked(False)

        self.cuda_on = False
        self.cuda_check = QCheckBox("Use CUDA GPU", self)
        self.cuda_check.toggled.connect(self.updateCuda)
        self.cuda_check.setChecked(False)

        # Choosing output folder name
        self.output_folder_label = QLabel("Give the output folder a name:")
        self.output_folder_box = QLineEdit(self)

        # Video options :
        self.video_label = QLabel(
            "If there are videos, choose how video files are handled, else ignore: "
        )
        self.video_status = "Save Average"

        self.video_choice = QComboBox(self)
        # live_button.clicked.connect(self.liveCommand)
        videochoices = [
            "Save Average",
            "Save Tif Stack",
            "Save Tif Sequence",
            "Save Video as .mp4",
            "Save video as .avi",
            "Save MotionCorrected Average",
        ]

        self.video_choice.addItems(videochoices)
        self.video_choice.currentTextChanged.connect(self.video_choice_changed)

        self.doc_label1 = QLabel("Document Section")
        self.doc_label1.setObjectName("doc_label")
        self.doc_label1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.doc_label = QLabel(
            "Following generation of images/videos, use this section to create \n an html or pdf file to display the resulting images:"
        )
        self.title_box_label = QLabel("Give a title for the experiment:")
        self.title_box = QLineEdit()
        self.notes_box_label = QLabel("Add some notes here:")
        self.notes_box = QTextEdit()

        # Call other functions
        self.make_buttons()
        # self.video_checkbox_functions()

        self.set_layouts()
        self.add_styles()
        self.set_fonts()
        self.show()

    def make_buttons(self):
        # folder browse button
        self.FolderBrowse_button = QPushButton("Choose Folder", self)
        self.FolderBrowse_button.clicked.connect(self.FileFolderChooser)

        # self.FolderBrowse_button.setStyleSheet("background-color : White")

        # Run button
        self.Run_button = QPushButton("Run!", self)
        self.Run_button.clicked.connect(self.RunCommand)

        # html button
        self.html_button = QPushButton("Make HTML!")
        self.html_button.clicked.connect(self.html_command)

        # pdf button
        self.pdf_button = QPushButton("Make PDF!")
        self.pdf_button.clicked.connect(self.pdf_command)

        # stop button
        self.stopButton = QPushButton("Stop Process")
        self.stopButton.clicked.connect(self.stopCommand)
        self.stopButton.setObjectName("stopButton")
        self.stopSignal = False

    def add_styles(self):
        # app.setStyleSheet(" QCheckBox{font-size: 14pt;}")
        # app.setStyleSheet("QPushButton{background-color:White;font-size:16pt;font-weight:500;}")
        app.setStyleSheet(
            """*{font-family:"helvetica", serif; font-weight:200} QWidget{background-color:#C2E4E9;} \
            QPushButton:hover{background-color: #D8BBEA; color:black;} \
            QPushButton{background-color:white;font-size:16pt;font-weight:500; color:black;}  \
            QPushButton.active{background-color:#502673}
            QCheckBox{background-color:white;font-size: 11pt; color:black; } \
            QLabel{font-size:12pt;font-weight:400; color:black; }\
            QComboBox{background-color:white;font-size:10px;vertical-align:text-top; color:black;}\
            QTextEdit{background-color:white; color:black;} \
            QLineEdit{background-color:white; color:black;}\
            #stopButton:hover{background-color:#F2B8D5; color:black;}\
            QLabel#title{font-size:18pt; font-weight:700; color:black;}\
            QLabel#doc_label{font-size:15pt; font-weight:600; color:black;}
            """
        )

    def set_fonts(self):
        # define title font
        self.titlefont = QFont()
        self.titlefont.setPointSize(20)
        self.titlefont.setBold(True)
        # add title font to title and doc section title
        self.title.setFont(self.titlefont)
        self.doc_label1.setFont(self.titlefont)

        # define and set video label font
        self.video_labelfont = QFont()
        self.video_labelfont.setPointSize(12)
        self.video_labelfont.setItalic(True)
        self.video_label.setFont(self.video_labelfont)

        # define button font - Easier done in the add_styles method

        # self.button_font = QFont()
        # self.button_font.setPointSize(16)
        # self.button_font.setBold(True)
        # self.button_font.setItalic(True)

        # set button fonts
        # self.FolderBrowse_button.setFont(self.button_font)
        # self.Run_button.setFont(self.button_font)
        # self.html_button.setFont(self.button_font)
        # self.pdf_button.setFont(self.button_font)

    def set_layouts(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        i = 0
        self.layout.addWidget(self.title, i, 0, 1, 2)
        i+=1
        self.layout.addWidget(self.folderlabel, i, 0, 1, 1)
        self.layout.addWidget(self.live_choice, i, 1, 1, 1)
        i+=1
        self.layout.addWidget(self.FolderBrowse_button, i, 0, 1, 2)
        i+=1
        self.layout.addWidget(self.folderpath_label, i, 0, 1, 2)
        i+=1
        self.layout.addWidget(self.filepattern_label, i, 0, 1, 1)
        self.layout.addWidget(self.filepattern_box, i, 1, 1, 1)
        i+=1
        self.layout.addWidget(self.contrast_check, i, 0,1,1)
        i+=1
        self.layout.addWidget(self.med_check, i, 0, 1, 1)
        self.layout.addWidget(self.med_choice, i, 1, 1, 1)
        i+=1
        self.layout.addWidget(self.gauss_check, i, 0, 1, 1)
        self.layout.addWidget(self.gauss_choice, i, 1, 1, 1)
        i+=1
        self.layout.addWidget(self.bin_check, i, 0, 1, 1)
        self.layout.addWidget(self.bin_choice, i, 1, 1, 1)
        i+=1
        self.layout.addWidget(self.scalebar_check, i, 0, 1, 1)
        i+=1
        self.layout.addWidget(self.output_type_label, i,0,1,1)
        self.layout.addWidget(self.output_choice, i, 1, 1,1)
        i+=1
        self.layout.addWidget(self.topaz_label, i, 0, 1, 2)
        i+=1
        self.layout.addWidget(self.topaz_check, i, 0, 1, 1)
        self.layout.addWidget(self.cuda_check, i, 1, 1, 1)
        i+=1
        self.layout.addWidget(self.output_folder_label, i, 0, 1, 1)
        self.layout.addWidget(self.output_folder_box, i, 1, 1, 1)
        i+=1
        self.layout.addWidget(self.video_label, i, 0, 1, 2)
        i+=1
        self.layout.addWidget(self.video_choice, i, 0, 1, 2)
        i+=2
        # self.layout.addWidget(self.video_option1,9,0,1,1)
        # self.layout.addWidget(self.video_option2,9,1,1,1)
        # self.layout.addWidget(self.video_option3,10,0,1,1)
        # self.layout.addWidget(self.video_option4,10,1,1,1)
        self.layout.addWidget(self.Run_button, i, 0, 2, 2)
        i+=2
        self.layout.addWidget(self.stopButton, i, 0, 1, 2)
        i+=1
        self.layout.addWidget(self.doc_label1, i, 0, 1, 2)
        i+=1
        self.layout.addWidget(self.doc_label, i, 0, 1, 2)
        i+=1
        self.layout.addWidget(self.title_box_label, i, 0, 1, 1)
        i+=1
        self.layout.addWidget(self.title_box, i, 0, 1, 2)
        i+=1
        self.layout.addWidget(self.notes_box_label, i, 0, 1, 1)
        i+=1
        self.layout.addWidget(self.notes_box, i, 0, 1, 3)
        i+=4
        self.layout.addWidget(self.html_button, i, 0, 1, 1)
        self.layout.addWidget(self.pdf_button, i, 1, 1, 1)

    def video_checkbox_functions(self):
        # Video options checkboxes:
        self.video_group = QButtonGroup()

        self.video_option1 = QCheckBox("Save Average", self)
        self.video_option2 = QCheckBox("Save Video as mp4", self)
        self.video_option3 = QCheckBox("Save Tif Stack", self)
        self.video_option4 = QCheckBox("Save MotionCorrected average", self)
        self.video_group.buttonClicked.connect(self.video_group_func)
        self.video_status = "Save Average"
        self.video_group.addButton(self.video_option1)
        self.video_group.addButton(self.video_option2)
        self.video_group.addButton(self.video_option3)
        self.video_group.addButton(self.video_option4)

    def stopCommand(self):
        self.stopSignal = True
        print("Stopping before next file")

    def eval_stop(self):
        if self.stopSignal == True:
            print("Stop signal recieved, exiting now")
            self.stopSignal = False
            return True

    def update_contrast(self, state):
        self.contrast_state=state

    def text_changed(self, s):  # i is an int
        self.folder_option = s

    def med_int_changed(self, i):
        self.med_filter_value = int(i)

    def gauss_int_changed(self, i):
        self.gauss_filter_value = int(i)

    def bin_int_changed(self, i):
        self.bin_value = int(i)

    def updateGauss(self, state):
        self.Gauss_state = state

    def updateMed(self, state):
        self.Med_state = state

    def updateBin(self, state):
        self.Bin_state = state

    def output_choice_changed(self, s):
        self.output_type=s
    def updateScalebar(self, state):
        self.scalebar_on = state

    def video_group_func(self, but):
        self.video_status = but.text()

    def video_choice_changed(self, s):
        self.video_status = s

    def updateTopaz(self, state):
        self.topaz_on = state

    def updateCuda(self, state):
        self.cuda_on = state

    def FileFolderChooser(self):
        if self.folder_option == "Folder" or self.folder_option == "Live Processing":
            self.folderpath = QFileDialog.getExistingDirectory(self, "Select a Folder")
        else:
            self.folderpath = QFileDialog.getOpenFileName(self, "Select a File")[0]
        self.folderpath_label.setText(self.folderpath)

    def html_command(self):
        outdir = self.output_folder_box.text()

        if outdir == "":
            outdir = "."

        if self.folderpath == "" or self.folderpath == None:
            print("Please select a folder/file")
            return 1

        cwd = os.getcwd()
        os.chdir(self.folderpath + "/" + outdir)

        title = self.title_box.text()
        if title == "":
            title = "Default_title"
        notes = self.notes_box.toPlainText()
        print("Writing html and css files")
        try:
            image_files, video_files = get_files_html("Images", "Videos")
        except FileNotFoundError:
            print(
                "The Images folder was not found, please make sure that the output folder defined above has a folder of images called images."
            )
            os.chdir(cwd)
            return 1
        print(image_files)

        write_html(image_files, video_files, title, notes)
        write_css()
        print("Done!")
        os.chdir(cwd)

    def pdf_command(self):
        outdir = self.output_folder_box.text()
        if outdir == "":
            outdir = "."

        if self.folderpath == "" or self.folderpath == None:
            print("Please select a folder/file")
            return 1

        cwd = os.getcwd()
        os.chdir(self.folderpath + "/" + outdir)

        title = self.title_box.text()
        notes = self.notes_box.toPlainText()

        print(os.getcwd())
        print(os.listdir("."))
        try:
            images = ["Images/" + x for x in os.listdir("Images") if "jpg" in x]
        except FileNotFoundError:
            print(
                "The Images folder was not found, please make sure that the output folder defined above has a folder of images called images."
            )
            os.chdir(cwd)
            return 1
        print(images)
        try:
            pdf_generator(images, title, notes)
        except Exception as e:
            print("Error! Not sure what has happened here")
            print(e)
        os.chdir(cwd)

    def RunCommand(self):
        # print('Gauss=', self.Gauss_state)
        # print('Med=',self.Med_state)
        # print('med_value',self.med_filter_value)
        # print('Bin=',self.Bin_state)
        # print('Folder:' ,self.folder_option)

        outdir = self.output_folder_box.text()
        if outdir == "":
            outdir = "."
        elif "\n" in outdir:
            outdir.replace("\n", "")

        if self.Med_state == False:
            self.med_filter_value = 0
        if self.Gauss_state == False:
            self.gauss_filter_value = 0
        if self.Bin_state == False:
            self.bin_value = 0

        if self.folderpath == "" or self.folderpath == None:
            print("Please select a folder/file")
            return 1
        print(self.folderpath)
        print('Contrast_state', self.contrast_state)
        try:
            if self.folder_option == "Folder":
                print("Running folder?")
                thread = threading.Thread(
                    target=self.process_folder,
                    args=(
                        self.folderpath,
                        outdir,
                        self.output_type,
                        self.contrast_state,
                        self.bin_value,
                        self.med_filter_value,
                        self.gauss_filter_value,
                        self.scalebar_on,
                        self.video_status,
                        self.topaz_on,
                        self.cuda_on,
                    ),
                )
                thread.start()
            elif self.folder_option == "File":
                print(self.live)
                self.process_file(
                    self.folderpath,
                    outdir,
                    self.output_type,
                    self.contrast_state,
                    self.bin_value,
                    self.med_filter_value,
                    self.gauss_filter_value,
                    self.scalebar_on,
                    self.video_status,
                    self.topaz_on,
                    self.cuda_on,
                )
            elif self.folder_option == "Live Processing":
                # live_process_folder(self.folderpath, outdir, self.bin_value, self.med_filter_value, self.gauss_filter_value,self.video_status )
                print("Live processing")
                thread = threading.Thread(
                    target=self.live_process,
                    args=(
                        self.folderpath,
                        outdir,
                        self.output_type,
                        self.contrast_state,
                        self.bin_value,
                        self.med_filter_value,
                        self.gauss_filter_value,
                        self.scalebar_on,
                        self.video_status,
                        self.topaz_on,
                        self.cuda_on,
                    ),
                )
                thread.start()
        except Exception as e:
            print(
                "Whoops there is an error, check the terminal and your inputs and try again."
            )
            print(e)

    def process_folder(
        self,
        folder,
        output_folder_name,
        output_type,
        contrast_state,
        xybin,
        medfilter,
        gaussian_filter,
        scalebar_on,
        video_status,
        topaz_on,
        cuda_on,
    ):
        start_time = time.time()
        print("Processing folder!")
        cwd = os.getcwd()

        os.chdir(folder)

        #        dm_files = [x for x in os.listdir('.') if x[-4:-1]=='.dm']
        #        dm_vids = [x for x in dm_files if isvideo(x)]
        #        dm_frames = [x for x in dm_files if x[-9]=='-' and x[-13:-9].isdigit() and x[-8:-4].isdigit()]
        #        dm_ims = [x for x in dm_files if x not in dm_vids and x not in dm_frames]

        pattern = self.filepattern_box.text()
        if pattern == "":
            pattern = "*dm*"
        im_files, vid_files, dm_frames = get_files_from_pattern(pattern)

        print("Imfiles", im_files)
        print("Vidfiles", vid_files)
        print("dm_frames", dm_frames)

        if output_folder_name not in os.listdir(".") and output_folder_name != ".":
            os.mkdir(output_folder_name)

        for file in vid_files:
            print(self.stopSignal)
            if self.eval_stop():
                return 1
            print("Processing: ", file)
            video_processing(
                filename=file,
                output_folder_name=output_folder_name,
                output_type=output_type,
                contrast_enhance=contrast_state,
                xybin=xybin,
                medfilter=medfilter,
                gaussian_filter=gaussian_filter,
                scalebar_on=scalebar_on,
                video_status=video_status,
                topaz_denoise=topaz_on,
                denoise_with_cuda=cuda_on,
            )

        for file in im_files:
            if self.eval_stop():
                return 1
            default_image_pipeline(
                file,
                output_type=output_type,
                contrast_enhance=contrast_state,
                xybin=xybin,
                medfilter=medfilter,
                gaussfilter=gaussian_filter,
                scalebar=scalebar_on,
                outdir=output_folder_name,
                topaz_denoise=topaz_on,
                denoise_with_cuda=cuda_on,
            )
        if len(dm_frames) != 0:
            print(dm_frames)
            frames_processing(
                dm_frames,
                output_folder_name,
                output_type,
                xybin,
                medfilter,
                gaussian_filter,
                video_status,
            )
        print("All files in folder complete!")
        running_time = time.time() - start_time
        print(
            "Running time for {} images and {} videos: {}".format(
                len(im_files), len(vid_files), running_time
            )
        )
        os.chdir(cwd)

    def live_process(
        self,
        folder,
        output_folder_name,
        output_type,
        contrast_state,
        xybin,
        medfilter,
        gaussian_filter,
        scalebar_on,
        video_status,
        topaz_on,
        cuda_on,
    ):
        cwd = os.getcwd()
        # print('calling function')
        os.chdir(folder)
        files = os.listdir(".")
        file_set = set(files)
        start_time = time.time()
        max_running_time = 3600
        # print(os.getcwd())
        if output_folder_name not in os.listdir(".") and output_folder_name != ".":
            os.mkdir(output_folder_name)

        pattern = self.filepattern_box.text()
        if pattern == "":
            pattern = "*dm*"

        possible_filetypes = [
            ".avi",
            ".mp4",
            ".dm3",
            ".dm4",
            ".tif",
            ".jpg",
        ]

        while True:
            if self.eval_stop():
                return 1

            im_files, vid_files, dm_frames = get_files_from_pattern(pattern)

            for file in im_files + vid_files + dm_frames:
                if file not in file_set:
                    # print(file)
                    if file[-4:].lower() in possible_filetypes:
                        # this is to check the file isnt still being written, if it grows in size, it ignores if for now and loops again:
                        currentsize = os.path.getsize(file)
                        time.sleep(1)
                        if os.path.getsize(file) > currentsize:
                            break

                        if isvideo(file) and video_status != "Save Average":
                            video_processing(
                                file,
                                output_folder_name,
                                output_type,
                                contrast_state,
                                xybin,
                                medfilter,
                                gaussian_filter,
                                scalebar_on=scalebar_on,
                                video_status=video_status,
                                topaz_denoise=topaz_on,
                                denoise_with_cuda=cuda_on,
                            )
                        else:
                            default_image_pipeline(
                                file,
                                output_type=output_type,
                                xybin=xybin,
                                contrast_enhance=contrast_state,
                                medfilter=medfilter,
                                gaussfilter=gaussian_filter,
                                outdir=output_folder_name,
                                topaz_denoise=topaz_on,
                                denoise_with_cuda=cuda_on,
                            )

                    file_set.add(file)

            running_time = time.time() - start_time
            print("Running time : {}s".format(round(running_time, 0)))

            if running_time > max_running_time:
                break
            time.sleep(10)
            # print('Looping')
        print("Time out reached, exiting now")
        os.chdir(cwd)

    def process_file(
        self,
        file,
        outdir,
        output_type,
        contrast_state,
        bin_value,
        med_filter_value,
        gauss_filter_value,
        scalebar_on,
        video_status,
        topaz_on, 
        cuda_on
    ):
        cwd = os.getcwd()
        wd = '/'.join(file.split('/')[:-1])
        os.chdir(wd)
        if isvideo(file):
            video_processing(
                file,
                outdir,
                output_type,
                contrast_state,
                xybin=bin_value,
                medfilter=med_filter_value,
                gaussian_filter=gauss_filter_value,
                scalebar_on=scalebar_on,
                video_status=video_status,
                topaz_denoise=topaz_on,
                denoise_with_cuda=cuda_on,
            )
        else:
            default_image_pipeline(
                file,
                output_type=output_type,
                contrast_enhance=contrast_state,
                xybin=bin_value,
                medfilter=med_filter_value,
                gaussfilter=gauss_filter_value,
                scalebar=scalebar_on,
                outdir=outdir,
                topaz_denoise=topaz_on,
                denoise_with_cuda=cuda_on
            )
        os.chdir(cwd)



# MainApplication.show()
# application.exec()
app = QApplication(sys.argv)
ex = MainApplication()
sys.exit(app.exec())
