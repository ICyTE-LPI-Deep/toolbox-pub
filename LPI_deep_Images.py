###############################################################################
#                         ICyTE-LPI-Deep Toobox                               #
# module name:                                                                #
#     LPI_deep_Images                                                         #
#                                                                             #
# module description:                                                         #
#     This module contains all the required functions for processing images.  #
#                                                                             #
# authors of the toolbox:                                                     #
#     Agustín Amalfitano                                                      #
#     Diego Comas				                       						  #
#     Franco Ercoli				                       						  #
#     Juan Iturriaga    		                       						  #
#                                                                             #  
# colaborators:                                                               #
#     Luciana Simón Gonzalez                        						  #
#     Virginia Ballarin			                       						  #
#     Gustavo Meschino			                       						  #
#                                                                             #
# versions:                                                                   #
#     module: 1.0 - 2023-05-10                                                #
#     toolbox 1.0 - 2023-XX-XX                                                #
#                                                                             #
# *LPI-ICyTE-CONICET-UMDP                                                     #
#                                                                             #
###############################################################################

# ******************************************************************************
# ------------------------------LIST OF VERSIONS--------------------------------
# Version |   Date   |         Authors      | Description
# -------- ---------- ---------------------- -----------------------------------
#
#    1.0   05/10/2023  Diego Comas            First version.
#
# ******************************************************************************

# ------------------------------LIST OF FUNCTIONS-------------------------------
# Functions              |   Date    |    Authors          |   Description
# ------------------------------------------------------------------------------
# apply_aug_offline       05/10/2023   Diego Comas          This function 
#                                                           generates an 
#                                                           augmentation 
#                                                           generador from 
#                                                           "imgaug" toolbox.
#
# apply_aug_offline       05/10/2023   Diego Comas          This function applies 
#                                                           offline augmentation 
#                                                           to all the images in 
#                                                           a folder from an 
#                                                           augmentation object.
#
# ------------------------------------------------------------------------------

# --------------------------IMPORTS---------------------------------------------
# Reserved.

# ------------------------------------------------------------------------------
def augmentation_generator(augmentation_type):
    """
     This function generates an augmentation generador from "imgaug" toolbox.

         --Inputs:
    
        augmentation_type = A NUMBER indicating the type of augmentation to apply.
            1 --> Augmentation including sequential application of horizontal flipping, 
                  constrast normalization, brightness, scale, translations, and rotation.    
    
    --Outputs:
        
        augmentor = An OBJECT with the transformations generated from "imgaug" toolbox.
        
    """

    # Libraries:
    import imgaug.augmenters as iaa
    
    # Analizing the augmentation type in order to create the object "augmentor":
    if augmentation_type == 1:
        # Defines sequential augmentation:
        augmentor = iaa.Sequential([
            iaa.Flipud(0.5), # horizontal flips
            iaa.LinearContrast((0.75, 1.5)), # contrast normalization
            iaa.Multiply((0.8, 1.2), per_channel=0.2), # adjust brightness
            iaa.Affine(
                scale={"x": (0.75, 1.0), "y": (0.75, 1.0)},
                translate_percent={"x": (-0.05, 0.05), "y": (-0.05, 0.05)},
                rotate=(-5, 5),
            ) # random affine transformations
        ], random_order=True)

    # Returning outputs:
    return augmentor

# ------------------------------------------------------------------------------
def apply_aug_offline(input_path, output_path, augmentor, number_transformations, image_extension):
    """
     This function applies offline augmentation to all the images in a folder from a "augmentor" 
     object generated from "augmentation_generator" or "imgaug" toolbox.

         --Inputs:
    
        input_path = A STRING with the full path of the original images.
        
        output_path = A STRING with the full path of the output images.

        augmentor = An OBJECT with the transformations generated using 
                    "augmentation_generator" or "imgaug" toolbox.
    
        number_transformations = A NUMBER indicating the number of images to generates for 
                                 each image in the "input_path".

        image_extension = A STRING with the extension of images files to be augmented.
    
    --Outputs:
        
        None.
        
    """

    # Libraries:
    import imgaug.augmenters as iaa
    import cv2
    import os
    from LPI_deep_Files import create_folder

    # Create the output directory:
    create_folder(output_path)

    # loop through all images in the input directory
    for filename in os.listdir(input_path):
        if filename.endswith('.'+image_extension): # check if the file is an image
            # load the image
            img = cv2.imread(os.path.join(input_path, filename))

            # generate augmented images for this image:
            for i in range(number_transformations):
                # Apply the augmentation sequence to the image:
                aug_img = augmentor(image=img)

                # Save the augmented image:
                output_image_name = filename[:-(len(image_extension)+1)] + '_' + str(i) + '.' + image_extension
                output_filename = os.path.join(output_path, output_image_name)
                cv2.imwrite(output_filename, aug_img)

# ------------------------------------------------------------------------------
