#image_viewer.pyw

from bin.settings import SettingsDialog
from bin.utility import OutlinedLabel
from bin.SettingsManager import SettingsManager
from bin.utility import dark_palette, light_palette, dark_palette_2, light_palette_2
import os
#import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QWIDGETSIZE_MAX, QShortcut, QToolTip, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPalette, QColor, QKeySequence, QMovie, QFont, QBrush, QPainterPath, QPen
from PyQt5.QtCore import QDir, Qt, QSize, QTimer
from PyQt5 import QtCore
import shutil

class ImageViewer(QMainWindow):
    def __init__(self, initialDir=None):
        super().__init__()

        # Determine the base directory of the script
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Update paths to use absolute paths
        icon_path = os.path.join(base_dir, 'images', 'icon.png')
        next_icon_path = os.path.join(base_dir, 'images', 'next.png')
        back_icon_path = os.path.join(base_dir, 'images', 'back.png')
        favorite_icon_path = os.path.join(base_dir, 'images', 'favorite.png')
        edit_icon_path = os.path.join(base_dir, 'images', 'edit.png')
        self.edit_icon_path = os.path.join(base_dir, 'images', 'edit.png')
        add_icon_path = os.path.join(base_dir, 'images', 'add.png')
        clear_icon_path = os.path.join(base_dir, 'images', 'clear.png')
        hide_icon_path = os.path.join(base_dir, 'images', 'hide.png')
        delete_icon_path = os.path.join(base_dir, 'images', 'delete.png')
        settings_icon_path = os.path.join(base_dir, 'images', 'settings.png')
        move_icon_path = os.path.join(base_dir, 'images', 'move.png')
        icon_icon_path = os.path.join(base_dir, 'images', 'icon.png')
        self.nodirectory_icon_path = os.path.join(base_dir, 'images', 'nodirectory.png')
        self.moved_icon_path = os.path.join(base_dir, 'images', 'moved.png')
        #back_icon_path = os.path.join(base_dir, 'images', 'back.png')
        # ... and so on for other images ...

        self.setWindowTitle("Quick Image Sorter")
        self.setWindowIcon(QIcon(icon_icon_path))
        self.setGeometry(100, 100, 800, 800)

        self.settingsManager = SettingsManager()
        self.show_filenames = self.settingsManager.get_setting("show_filenames")

        self.edits = set()
        self.hideSorted = False
        self.originalImages = []
        #self.show_filenames = True
        #self.load_settings()
        self.favoriteIcon = QPixmap(favorite_icon_path)

        self.imageFolder = initialDir if initialDir else ''
        self.images = []
        self.currentIndex = -1
        self.favorites = set()
        self.edits = set()

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setMinimumSize(1, 1)
        self.imageLabel.setMaximumSize(QSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX))
        self.imageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow label to expand
        self.imageLabel.setFocusPolicy(Qt.NoFocus)

        # Define apply_theme as an instance method
        self.apply_theme(QApplication.instance(), self.settingsManager.get_setting("theme"))

        # Filename label initialization with outlined text
        self.filenameLabel = OutlinedLabel(self.imageLabel)  # Use OutlinedLabel instead of QLabel
        self.filenameLabel.setAlignment(Qt.AlignCenter)
        self.filenameLabel.setFont(QFont("Arial", 14))
        self.filenameLabel.setMargin(10)

        # Bind the "1" key to toggle_show_filenames
        self.toggleFilenameShortcut = QShortcut(QKeySequence("1"), self)
        self.toggleFilenameShortcut.activated.connect(self.toggle_show_filenames)

        # Set font size and color
        font = QFont()
        font.setPointSize(14)  # Adjust the font size as needed
        self.filenameLabel.setFont(font)
        self.filenameLabel.setStyleSheet("color: white; border: black; background-color: rgba(0, 0, 0, 0);")
        self.filenameLabel.setMargin(10)  # Add some margin if needed

        # Set maximum size of the buttons to the size of the icons
        #icon_size = QSize(50, 50)

        # Initialize currentIconSize before creating buttons
        self.currentIconSize = self.icon_size_mapping(self.settingsManager.get_icon_size())

        self.nextButton = self.create_button(next_icon_path, "Next Image (Right Arrow)", "Right", self.next_image)
        self.prevButton = self.create_button(back_icon_path, "Previous Image (Left Arrow)", "Left", self.prev_image)
        self.favButton = self.create_button(favorite_icon_path, "Favorite (F)", "F", self.toggle_favorite)
        self.editButton = self.create_button(edit_icon_path, "Edit (E)", "E", self.toggle_edit)
        self.addDirButton = self.create_button(add_icon_path, "Add Directory (A)", "A", self.add_directory)
        self.clearButton = self.create_button(clear_icon_path, "Clear All (C)", "C", self.clear_all)
        self.hideButton = self.create_button(hide_icon_path, "Hide/Show All Sorted (H)", "H", self.hide_all_sorted)
        self.deleteButton = self.create_button(delete_icon_path, "Delete (Del)", "Del", self.delete_image)
        self.settingsButton = self.create_button(settings_icon_path, "Settings (S)", "S", self.open_settings_dialog)
        self.moveButton = self.create_button(move_icon_path, "Move Images (M)", "M", self.move_favorites)

        # Horizontal layout for other buttons with stretching
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()  # Add stretch before buttons

        # Add remaining buttons here in the middle
        buttonLayout.addWidget(self.favButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.addDirButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.hideButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.settingsButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.moveButton)
        buttonLayout.addStretch()  # Add stretch after buttons

        # Create the main vertical layout
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        mainLayout.addWidget(self.imageLabel)  # Add the image label
        mainLayout.addLayout(buttonLayout)  # Add the buttons layout

        # Create a central container widget and set the main layout
        centerContainer = QWidget()
        centerContainer.setLayout(mainLayout)
        self.setCentralWidget(centerContainer)

        self.show()  # Ensure the window is shown
        QApplication.processEvents()  # Process any pending events to update the layout

        self.load_images()

        self.update_ui_with_settings()

        self.updateButtonPositions()
        self.update_filename_label_position()

    def icon_size_mapping(self, size_text):
        size_dict = {
            "Small": 30,
            "Normal": 50,
            "Large": 70
        }
        return size_dict.get(size_text, 50)  # Default to "Normal" size

    def update_font_sizes(self):
        # Define font sizes based on icon size
        font_size = {
            "Small": 10,
            "Normal": 14,
            "Large": 18
        }.get(self.settingsManager.get_icon_size(), 14)

        # Update font size for filename label
        font = self.filenameLabel.font()
        font.setPointSize(font_size)
        self.filenameLabel.setFont(font)

    def update_ui_with_settings(self):
        self.currentIconSize = self.icon_size_mapping(self.settingsManager.get_icon_size())
        max_button_size = self.currentIconSize + 20

        # Update button icon sizes and maximum sizes
        for button in [self.nextButton, self.prevButton, self.favButton, self.editButton, self.addDirButton, self.clearButton, self.hideButton, self.deleteButton, self.settingsButton, self.moveButton]:
            button.setIconSize(QSize(self.currentIconSize, self.currentIconSize))
            button.setMaximumSize(QSize(max_button_size, max_button_size))
            
        self.update_font_sizes()


    def create_button(self, icon_path, tooltip_text, shortcut_key, callback):
        button = QPushButton(self.imageLabel)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(self.currentIconSize, self.currentIconSize))  # Set icon size based on currentIconSize
        button.setMaximumSize(QSize(self.currentIconSize, self.currentIconSize))
        button.setStyleSheet("""
            QPushButton {
                background: transparent; 
                border: none; 
                padding: 4px;
            }
            QPushButton:hover {
                border: 2px solid white;
                border-radius: 5px;
            }
        """)
        button.clicked.connect(callback)
        self.setButtonHoverStyle(button, tooltip_text)
        button.installEventFilter(self)
        if shortcut_key:
            shortcut = QShortcut(QKeySequence(shortcut_key), self)
            shortcut.activated.connect(callback)
        return button


    def apply_theme(self, app, theme):
        if theme == "Dark":
            app.setPalette(dark_palette())
        elif theme == "Light":
            app.setPalette(light_palette())
        elif theme == "Dark 2":
            app.setPalette(dark_palette_2())
        elif theme == "Light 2":
            app.setPalette(light_palette_2())
        # Add more themes as necessary

  
    def toggle_show_filenames(self):
        self.show_filenames = not self.show_filenames
        self.settingsManager.set_setting("show_filenames", self.show_filenames)
        self.show_image()

    def open_settings_dialog(self):
        dialog = SettingsDialog(self.settingsManager, self)
        if dialog.exec_():
            # Apply the selected theme
            theme = self.settingsManager.get_setting("theme")
            self.apply_theme(QApplication.instance(), theme)

            # Update and apply other settings
            self.show_filenames = self.settingsManager.get_setting("show_filenames")
            self.update_ui_with_settings()  # Update icon sizes and other UI elements

            # Refresh the image display
            self.show_image()

            # Force a resize event to update the layout
            self.resize(self.width(), self.height())

            # Process any pending events to update the layout
            QApplication.processEvents()

            self.updateButtonPositions()
            self.update_filename_label_position()
        else:
            print("Settings canceled")



    def updateButtonPositions(self):
        # Adjust these values as needed
        margin = 10  # Margin from the edges of the window
        buttonSize = self.currentIconSize  # Use the current icon size

        # Calculate the position for the prevButton
        prevButtonX = margin
        prevButtonY = (self.imageLabel.height() - buttonSize) // 2
        self.prevButton.setGeometry(prevButtonX, prevButtonY, buttonSize, buttonSize)

        # Calculate the position for the nextButton
        nextButtonX = self.imageLabel.width() - buttonSize - margin
        nextButtonY = (self.imageLabel.height() - buttonSize) // 2
        self.nextButton.setGeometry(nextButtonX, nextButtonY, buttonSize, buttonSize)


    def hide_all_sorted(self):
        if self.hideSorted:
            # Restore original images
            self.images = self.originalImages.copy()
        else:
            # Store the original images and hide sorted images
            self.originalImages = self.images.copy()
            self.images = [img for img in self.images if img not in self.favorites and img not in self.edits]

        self.hideSorted = not self.hideSorted  # Toggle the state
        if self.currentIndex >= len(self.images):
            self.currentIndex = len(self.images) - 1 if self.images else -1
        self.show_image()

    def delete_image(self):
        if self.currentIndex < 0 or self.currentIndex >= len(self.images):
            return

        current_image = self.images[self.currentIndex]

        reply = QMessageBox.question(self, 'Delete Image', f'Are you sure you want to delete "{os.path.basename(current_image)}"?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # Stop the QMovie if the current image is a GIF
                if current_image.lower().endswith('.gif'):
                    if self.imageLabel.movie():
                        self.imageLabel.movie().stop()
                        self.imageLabel.setMovie(None)

                os.remove(current_image)
                del self.images[self.currentIndex]
                self.currentIndex = max(0, self.currentIndex - 1)  # Adjust index since an image is removed
                self.show_image()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'An error occurred while deleting the file: {e}')

    def clear_all(self):
        # Confirmation dialog
        reply = QMessageBox.question(self, 'Clear All', 'Are you sure you want to clear all items?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.images.clear()
            self.currentIndex = -1
            self.favorites.clear()
            self.edits.clear()
            self.show_image()
        else:
            # User chose 'No', so don't clear anything
            pass

    def add_directory(self):
        new_dir = QFileDialog.getExistingDirectory(self, "Select Additional Directory")
        if new_dir:
            new_images = [os.path.join(new_dir, f) for f in os.listdir(new_dir) if os.path.isfile(os.path.join(new_dir, f))]
            self.images.extend(new_images)
            self.currentIndex = max(0, self.currentIndex)  # Update current index if it was -1
            self.show_image()

    def load_images(self):
        try:
            if not self.imageFolder:
                self.imageFolder = QFileDialog.getExistingDirectory(self, "Select Directory")
            
            if self.imageFolder:
                # Filter for common image file extensions
                image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
                self.images = [os.path.join(self.imageFolder, f) for f in os.listdir(self.imageFolder) 
                            if os.path.isfile(os.path.join(self.imageFolder, f)) and 
                            os.path.splitext(f)[1].lower() in image_extensions]
                
                self.originalImages = self.images.copy()  # Store the original list of images

                if not self.images:
                    self.show_no_images_placeholder()
                else:
                    self.currentIndex = 0
                    self.show_image()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error loading images: {e}')


    def show_no_images_placeholder(self):
        # Function to show the 'no directory' placeholder and disable buttons
        no_directory_placeholder_path = self.nodirectory_icon_path
        pixmap = QPixmap(no_directory_placeholder_path)
        self.imageLabel.setPixmap(pixmap)
        self.favButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.currentIndex = -1

    def show_image(self):
        # Clear any existing GIF overlays
        self.clear_gif_overlays()

        # Placeholder paths
        no_directory_placeholder_path = self.nodirectory_icon_path
        moved_placeholder_path = self.moved_icon_path

        # Check if there are images in the list
        if not self.images:
            pixmap = QPixmap(no_directory_placeholder_path)
            self.imageLabel.setPixmap(pixmap)
            self.favButton.setEnabled(False)
            self.editButton.setEnabled(False)
            self.filenameLabel.setText("")  # Clear filename label
            self.filenameLabel.setVisible(False)  # Hide filename label
            return

        # Check if the current index is valid
        if 0 <= self.currentIndex < len(self.images):
            image_path = self.images[self.currentIndex]

            # Check if the current image exists
            if not os.path.exists(image_path):
                image_path = moved_placeholder_path
                self.favButton.setEnabled(False)
                self.editButton.setEnabled(False)
            else:
                # Enable buttons for valid images
                self.favButton.setEnabled(True)
                self.editButton.setEnabled(True)

            # Show or hide filename based on setting
            self.filenameLabel.setVisible(self.show_filenames)

            if image_path.lower().endswith('.gif'):
                # Handling GIF images with QMovie
                movie = QMovie(image_path)
                self.imageLabel.setMovie(movie)
                movie.start()
                self.overlay_icons_on_gif(image_path)  # Overlay icons on GIFs
            else:
                # Handling non-GIF images with QPixmap
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

                blank_pixmap = QPixmap(self.imageLabel.size())
                blank_pixmap.fill(Qt.transparent)

                painter = QPainter(blank_pixmap)
                x = (blank_pixmap.width() - scaled_pixmap.width()) // 2
                y = (blank_pixmap.height() - scaled_pixmap.height()) // 2
                painter.drawPixmap(x, y, scaled_pixmap)

                # Drawing icons on images (if applicable)
                self.overlay_icons_on_pixmap(painter, image_path)

                painter.end()
                self.imageLabel.setPixmap(blank_pixmap)

            # Update filename label
            self.filenameLabel.setText(os.path.basename(image_path))

            # Update filename label positioning
            self.updateButtonPositions()
            self.update_filename_label_position()

        else:
            # Invalid index or no directory selected
            pixmap = QPixmap(no_directory_placeholder_path)
            self.imageLabel.setPixmap(pixmap)
            self.favButton.setEnabled(False)
            self.editButton.setEnabled(False)
            self.filenameLabel.setText("")  # Clear filename label

    def overlay_icons_on_pixmap(self, painter, image_path):
        icon_size = QSize(75, 75)
        if self.currentIndex >= 0:
            if image_path in self.favorites:
                resized_favorite_icon = self.favoriteIcon.scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                x_icon = 10
                y_icon = 10
                painter.drawPixmap(x_icon, y_icon, resized_favorite_icon)

            if image_path in self.edits:
                edit_icon = QPixmap(self.edit_icon_path)
                resized_edit_icon = edit_icon.scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                x_edit_icon = 10
                y_edit_icon = 95
                painter.drawPixmap(x_edit_icon, y_edit_icon, resized_edit_icon)

    def overlay_icons_on_gif(self, image_path):
        # Clear previous icons if any
        self.clear_gif_overlays()

        # Calculate positions for the icons
        icon_size = QSize(75, 75)
        x_icon = 10
        y_icon = 10
        x_edit_icon = 10
        y_edit_icon = 95

        # Create and position the favorite icon if the image is favorited
        if image_path in self.favorites:
            self.favoriteOverlay = QLabel(self.imageLabel)
            self.favoriteOverlay.setPixmap(self.favoriteIcon.scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.favoriteOverlay.setGeometry(x_icon, y_icon, icon_size.width(), icon_size.height())
            self.favoriteOverlay.show()

        # Create and position the edit icon if the image is marked for edit
        if image_path in self.edits:
            self.editOverlay = QLabel(self.imageLabel)
            edit_icon = QPixmap(self.edit_icon_path)  # Use self.edit_icon_path instead of edit_icon_path
            self.editOverlay.setPixmap(edit_icon.scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.editOverlay.setGeometry(x_edit_icon, y_edit_icon, icon_size.width(), icon_size.height())
            self.editOverlay.show()

    def clear_gif_overlays(self):
        # Remove any existing overlays
        if hasattr(self, 'favoriteOverlay'):
            self.favoriteOverlay.deleteLater()
            del self.favoriteOverlay

        if hasattr(self, 'editOverlay'):
            self.editOverlay.deleteLater()
            del self.editOverlay

    def update_filename_label_position(self):
        bottom_offset = -15  # Adjust this value as needed
        padding = 10

        label_text = self.filenameLabel.text()
        label_width = self.filenameLabel.fontMetrics().boundingRect(label_text).width() + (2 * padding)
        label_height = self.filenameLabel.fontMetrics().height() + (2 * padding)

        label_x = int((self.imageLabel.width() - label_width) / 2)
        label_y = self.imageLabel.height() - label_height - bottom_offset

        self.filenameLabel.setGeometry(label_x, label_y, label_width, label_height)

    def resizeEvent(self, event):
        super(ImageViewer, self).resizeEvent(event)
        self.updateButtonPositions()
        self.update_filename_label_position()
        self.show_image()

    def next_image(self):
        if self.currentIndex < len(self.images) - 1:
            self.currentIndex += 1
            self.show_image()

    def prev_image(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.show_image()

    def toggle_favorite(self):
        if self.currentIndex < 0 or self.currentIndex >= len(self.images):
            return

        current_image = self.images[self.currentIndex]

        if not os.path.exists(current_image):
            print("This image has been moved and cannot be favorited.")
            return
        
        if current_image in self.favorites:
            self.favorites.remove(current_image)
        else:
            self.favorites.add(current_image)

        self.show_image()

    def toggle_edit(self):
        if self.currentIndex < 0 or self.currentIndex >= len(self.images):
            return

        current_image = self.images[self.currentIndex]

        if not os.path.exists(current_image):
            print("This image has been moved and cannot be edited.")
            return
        
        if current_image in self.edits:
            self.edits.remove(current_image)
        else:
            self.edits.add(current_image)

        self.show_image()

    def move_favorites(self):
        try:
            destination = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
            if destination:
                successful_moves = 0
                failed_moves = 0

                favorites_dest = os.path.join(destination, "Favorites")
                edits_dest = os.path.join(destination, "Edits")

                # Check if there are any favorites or edits to move
                if self.favorites:
                    favorites_dest = os.path.join(destination, "Favorites")
                    os.makedirs(favorites_dest, exist_ok=True)

                if self.edits:
                    edits_dest = os.path.join(destination, "Edits")
                    os.makedirs(edits_dest, exist_ok=True)

                # Move favorites
                for fav in list(self.favorites):
                    try:
                        # Stop the QMovie if the current image is a GIF and being displayed
                        if fav.lower().endswith('.gif') and fav == self.images[self.currentIndex]:
                            self.imageLabel.setMovie(None)

                        new_path = os.path.join(favorites_dest, os.path.basename(fav))
                        # Check if also in edits
                        if fav in self.edits:
                            # Duplicate the file for the edits folder
                            shutil.copy(fav, new_path)
                            new_edit_path = os.path.join(edits_dest, os.path.basename(fav))
                            shutil.move(fav, new_edit_path)  # This will remove the original after moving
                            self.edits.remove(fav)
                        else:
                            shutil.move(fav, new_path)
                        self.favorites.remove(fav)
                        successful_moves += 1
                    except Exception as e:
                        print(f"Failed to move {fav}: {e}")
                        failed_moves += 1

                # Refresh the display after moving files
                self.show_image()

                # Move edits (only those not already moved)
                for edit in list(self.edits):
                    try:
                        new_path = os.path.join(edits_dest, os.path.basename(edit))
                        shutil.move(edit, new_path)
                        self.edits.remove(edit)
                        successful_moves += 1
                    except Exception as e:
                        print(f"Failed to move {edit}: {e}")
                        failed_moves += 1

                if successful_moves:
                    print(f"Successfully moved {successful_moves} images.")
                if failed_moves:
                    print(f"Failed to move {failed_moves} images.")

                # Update the image list and index since files have been moved
                self.load_images()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while moving files: {e}')


    def setButtonHoverStyle(self, button, tooltip_text):
        button.setStyleSheet("""
            QPushButton {
                background: transparent; 
                border: none; 
                padding: 4px; 
            }
            QPushButton:hover {
                border: 2px solid white;
                border-radius: 5px;
            }
        """)
        button.setCursor(Qt.PointingHandCursor)

        # Set up timer for tooltip hover
        button.hoverTimer = QTimer(self)
        button.hoverTimer.setInterval(3000)  # 3000 milliseconds = 3 seconds
        button.hoverTimer.setSingleShot(True)
        button.hoverTimer.timeout.connect(
            lambda: self.showCustomToolTip(button, tooltip_text)
        )

        # Event filter to detect hover
        button.installEventFilter(self)

    def showCustomToolTip(self, button, text):
        # Custom tooltip position
        globalPos = button.mapToGlobal(QtCore.QPoint(0, 0))
        tooltipX = int(globalPos.x() + button.width() / 2)
        tooltipY = int(globalPos.y() - button.height() - 20)  # Adjust this value to move tooltip up
        QToolTip.showText(QtCore.QPoint(tooltipX, tooltipY), text)

    def eventFilter(self, source, event):
        if isinstance(source, QPushButton):
            if event.type() == QtCore.QEvent.Enter:
                source.hoverTimer.start()
            elif event.type() == QtCore.QEvent.Leave:
                source.hoverTimer.stop()
                QToolTip.hideText()
        return super(ImageViewer, self).eventFilter(source, event)

