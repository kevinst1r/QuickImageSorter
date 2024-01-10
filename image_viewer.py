#image_viewer.pyw

from settings import SettingsDialog
from utility import OutlinedLabel
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QWIDGETSIZE_MAX, QShortcut, QToolTip, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPalette, QColor, QKeySequence, QMovie, QFont, QBrush, QPainterPath, QPen
from PyQt5.QtCore import QDir, Qt, QSize, QTimer
from PyQt5 import QtCore
import shutil

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quick Image Sorter")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setGeometry(100, 100, 800, 800)

        self.edits = set()
        self.hideSorted = False
        self.originalImages = []
        self.show_filenames = True
        self.load_settings()
        self.favoriteIcon = QPixmap('images/favorite.png')
        self.imageFolder = ''
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
        icon_size = QSize(50, 50)

        # Create the 'Next' button with PNG icon
        self.nextButton = QPushButton(self.imageLabel)
        self.nextButton.setIcon(QIcon('images/next.png'))  # Set your PNG file path
        self.nextButton.setIconSize(icon_size)
        self.nextButton.setMaximumSize(icon_size)
        self.nextButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.nextButton.clicked.connect(self.next_image)
        self.nextButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.nextButton, "Next Image (Right Arrow)")
        self.nextImageShortcut = QShortcut(QKeySequence("Right"), self)
        self.nextImageShortcut.activated.connect(self.next_image)

        # Create the 'Previous' button with PNG icon
        self.prevButton = QPushButton(self.imageLabel)
        self.prevButton.setIcon(QIcon('images/back.png'))  # Set your PNG file path
        self.prevButton.setIconSize(icon_size)
        self.prevButton.setMaximumSize(icon_size)
        self.prevButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.prevButton.clicked.connect(self.prev_image)
        self.prevButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.prevButton, "Previous Image (Left Arrow)")
        self.prevImageShortcut = QShortcut(QKeySequence("Left"), self)
        self.prevImageShortcut.activated.connect(self.prev_image)

        # Create the 'Toggle Favorite' button with PNG icon
        self.favButton = QPushButton()
        self.favButton.setIcon(QIcon('images/favorite.png'))  # Set your PNG file path
        self.favButton.setIconSize(icon_size)
        self.favButton.setMaximumSize(icon_size)
        self.favButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.favButton.clicked.connect(self.toggle_favorite)
        self.favButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.favButton, "Favorite (F)")
        self.toggleFavShortcut = QShortcut(QKeySequence("F"), self)
        self.toggleFavShortcut.activated.connect(self.toggle_favorite)
        self.favButton.setEnabled(False)

        # Create the 'Toggle Edit' button with a new icon
        self.editButton = QPushButton()
        self.editButton.setIcon(QIcon('images/edit.png'))  # Set your PNG file path for the 'edit' icon
        self.editButton.setIconSize(icon_size)
        self.editButton.setMaximumSize(icon_size)
        self.editButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.editButton.clicked.connect(self.toggle_edit)
        self.editButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.editButton, "Edit (E)")
        self.toggleEditShortcut = QShortcut(QKeySequence("E"), self)
        self.toggleEditShortcut.activated.connect(self.toggle_edit)
        self.editButton.setEnabled(False)

        # Create the 'Add Directory' button with PNG icon
        self.addDirButton = QPushButton()
        self.addDirButton.setIcon(QIcon('images/add.png'))  # Set your PNG file path
        self.addDirButton.setIconSize(icon_size)
        self.addDirButton.setMaximumSize(icon_size)
        self.addDirButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.addDirButton.clicked.connect(self.add_directory)
        self.addDirButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.addDirButton, "Add Directory (A)")
        self.toggleAddShortcut = QShortcut(QKeySequence("A"), self)
        self.toggleAddShortcut.activated.connect(self.add_directory)

        # Create the 'Clear All' button with PNG icon
        self.clearButton = QPushButton()
        self.clearButton.setIcon(QIcon('images/clear.png'))  # Set your PNG file path
        self.clearButton.setIconSize(icon_size)
        self.clearButton.setMaximumSize(icon_size)
        self.clearButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.clearButton.clicked.connect(self.clear_all)
        self.clearButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.clearButton, "Clear All (C)")
        self.clearShortcut = QShortcut(QKeySequence("C"), self)
        self.clearShortcut.activated.connect(self.clear_all)

        # Create the 'Clear All Sorted' button with PNG icon
        self.clearSortedButton = QPushButton()
        self.clearSortedButton.setIcon(QIcon('images/hide.png'))  # Set your PNG file path
        self.clearSortedButton.setIconSize(icon_size)
        self.clearSortedButton.setMaximumSize(icon_size)
        self.clearSortedButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.clearSortedButton.clicked.connect(self.hide_all_sorted)
        self.clearSortedButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.clearSortedButton, "Hide/Show All Sorted (H)")
        self.clearSortedShortcut = QShortcut(QKeySequence("H"), self)
        self.clearSortedShortcut.activated.connect(self.hide_all_sorted)

        # Create the 'Delete' button with PNG icon
        self.deleteButton = QPushButton()
        self.deleteButton.setIcon(QIcon('images/delete.png'))  # Set your PNG file path for the 'delete' icon
        self.deleteButton.setIconSize(icon_size) 
        self.deleteButton.setMaximumSize(icon_size)
        self.deleteButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.deleteButton.clicked.connect(self.delete_image)
        self.deleteButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.deleteButton, "Delete (Del)")
        self.deleteShortcut = QShortcut(QKeySequence("Del"), self)
        self.deleteShortcut.activated.connect(self.delete_image)
        
        # Create the 'Delete' button with PNG icon
        self.settingsButton = QPushButton()
        self.settingsButton.setIcon(QIcon('images/settings.png'))
        self.settingsButton.setIconSize(icon_size)
        self.settingsButton.setMaximumSize(icon_size)
        self.settingsButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.settingsButton.clicked.connect(self.open_settings_dialog)
        self.settingsButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.settingsButton, "Settings (S)")
        self.settingsShortcut = QShortcut(QKeySequence("S"), self)
        self.settingsShortcut.activated.connect(self.open_settings_dialog)

        # Create the 'Move Favorites' button with PNG icon
        self.moveButton = QPushButton()
        self.moveButton.setIcon(QIcon('images/move.png'))  # Set your PNG file path
        self.moveButton.setIconSize(icon_size)
        self.moveButton.setMaximumSize(icon_size)
        self.moveButton.setStyleSheet("background: transparent; border: none; padding: 4px;")
        self.moveButton.clicked.connect(self.move_favorites)
        self.moveButton.setCursor(Qt.PointingHandCursor)
        self.setButtonHoverStyle(self.moveButton, "Move Images (M)")
        self.moveFavShortcut = QShortcut(QKeySequence("M"), self)
        self.moveFavShortcut.activated.connect(self.move_favorites)

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
        buttonLayout.addWidget(self.clearSortedButton)
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
        self.update_filename_label_position()  # Update the label position
        self.updateButtonPositions()

        self.load_images()

    def toggle_show_filenames(self):
        self.show_filenames = not self.show_filenames
        self.save_settings()  # Save the updated setting
        self.show_image()     # Refresh the image to reflect the change

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        
        # Load the current setting and update the checkbox
        dialog.filenameCheckbox.setChecked(self.show_filenames)

        if dialog.exec_():
            # Update the setting based on the checkbox state
            self.show_filenames = dialog.filenameCheckbox.isChecked()
            self.save_settings()  # Implement this method to save settings
            self.show_image()  # Refresh to apply the setting
        else:
            print("Settings canceled")

    def save_settings(self):
        settings_path = os.path.join(os.environ['APPDATA'], 'ECP Apps', 'QuickImageSorterSettings.json')
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)

        settings_data = {
            "show_filenames": self.show_filenames
        }

        with open(settings_path, 'w') as settings_file:
            json.dump(settings_data, settings_file, indent=4)

    def load_settings(self):
        settings_path = os.path.join(os.environ['APPDATA'], 'ECP Apps', 'QuickImageSorterSettings.json')

        if os.path.exists(settings_path):
            with open(settings_path, 'r') as settings_file:
                settings_data = json.load(settings_file)
                self.show_filenames = settings_data.get("show_filenames", True)
        else:
            self.show_filenames = True

    def updateButtonPositions(self):
        buttonSize = 50  # Define the size of your buttons
        prevButtonX = 10  # Left margin for prevButton
        prevButtonY = (self.imageLabel.height() - buttonSize) // 2
        self.prevButton.setGeometry(prevButtonX, prevButtonY, buttonSize, buttonSize)

        nextButtonX = self.imageLabel.width() - buttonSize - 10  # Right margin for nextButton
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

    def show_no_images_placeholder(self):
        # Function to show the 'no directory' placeholder and disable buttons
        no_directory_placeholder_path = 'images/nodirectory.png'
        pixmap = QPixmap(no_directory_placeholder_path)
        self.imageLabel.setPixmap(pixmap)
        self.favButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.currentIndex = -1

    def show_image(self):
        # Clear any existing GIF overlays
        self.clear_gif_overlays()

        # Placeholder paths
        no_directory_placeholder_path = 'images/nodirectory.png'
        moved_placeholder_path = 'images/moved.png'

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
                edit_icon = QPixmap('images/edit.png')
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
            edit_icon = QPixmap('images/edit.png')
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
        self.show_image()  # Update the image
        self.update_filename_label_position()  # Update the label position

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

    def setButtonHoverStyle(self, button, tooltip_text):
        button.setStyleSheet("""
            QPushButton {
                background: transparent; 
                border: none;
            }
            QPushButton:hover {
                border: 2px solid white;
                border-radius: 5px;
            }
        """)
        button.setCursor(Qt.PointingHandCursor)

        # Set up timer for hover
        button.hoverTimer = QTimer(self)
        button.hoverTimer.setInterval(2000)  # 1000 milliseconds = 1 second
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
        tooltipY = int(globalPos.y() - button.height() - 10)
        QToolTip.showText(QtCore.QPoint(tooltipX, tooltipY), text)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Enter and hasattr(source, 'hoverTimer'):
            source.hoverTimer.start()
        elif event.type() == QtCore.QEvent.Leave and hasattr(source, 'hoverTimer'):
            source.hoverTimer.stop()
        return super(ImageViewer, self).eventFilter(source, event)