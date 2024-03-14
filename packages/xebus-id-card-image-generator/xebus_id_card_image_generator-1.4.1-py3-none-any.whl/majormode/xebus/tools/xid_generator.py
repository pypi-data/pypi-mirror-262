# Copyright (C) 2020 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from __future__ import annotations

import logging
import math
import os
import re
from os import PathLike
from pathlib import Path

import qrcode
import unidecode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont
from majormode.perseus.utils import module_utils, cast
from majormode.xebus.constant import family_sheet
from majormode.xebus.utils import normalization_utils

from .model import IdCardInfo


# The default name and size of the font to render the owner's full name
# on their ID card.
DEFAULT_FONT_NAME = 'Calibri Bold'
DEFAULT_FONT_SIZE = 56
DEFAULT_FONT_MAXIMAL_SIZE = 70
DEFAULT_FONT_MINIMAL_SIZE = 48

# Default relative path of the folder where the font files are stored in.
DEFAULT_FONT_RELATIVE_PATH = 'fonts'

# The default file name format of an ID card.
#
# :todo: We need to support a file name format for ID cards other than
#     for children.
DEFAULT_ID_CARD_FILE_NAME_FORMAT = "{Class Name}_{SIS ID}_{Full Name}"

# Default size in pixels of an ID card.
DEFAULT_ID_CARD_WIDTH = 540
DEFAULT_ID_CARD_HEIGHT = 860
DEFAULT_ID_CARD_RATIO = DEFAULT_ID_CARD_WIDTH / DEFAULT_ID_CARD_HEIGHT
DEFAULT_ID_CARD_MAXIMUM_STANDARD_DEVIANCE = 0.01

DEFAULT_LINE_SPACING = 12

# The list of attribute names that can be used to name an ID card file.
ID_CARD_FILE_NAME_ATTRIBUTE_NAMES = [
    family_sheet.DEFAULT_FIELD_NAME_ACCOUNT_SIS_ID,
    family_sheet.DEFAULT_FIELD_NAME_CLASS_NAME,
    family_sheet.DEFAULT_FIELD_NAME_FIRST_NAME,
    family_sheet.DEFAULT_FIELD_NAME_FULL_NAME,
    family_sheet.DEFAULT_FIELD_NAME_GRADE_NAME,
    family_sheet.DEFAULT_FIELD_NAME_LAST_NAME,
]

# Define the absolute path to the data of this Python library.
#
# The data of this Python library are located in a folder ``data`` located
# at the root path of this Python library.
#
# We have organized our Python modules in a source folder ``src`` located
# at the root path of this Python library, therefore the source depth is
# ``1`` (not ``0``).
LIBRARY_DATA_PATH = os.path.join(
    module_utils.get_project_root_path(__file__, __name__, 1),
    'data'
)

# The regular expressions to validate the file name format of an ID card.
REGEX_PATTERN_ID_CARD_ATTRIBUTE_NAME = r'{([a-z\s#]+)}'
REGEX_ID_CARD_ATTRIBUTE_NAME = re.compile(REGEX_PATTERN_ID_CARD_ATTRIBUTE_NAME, flags=re.IGNORECASE)


def __calculate_full_name_optimal_font_size(
        full_name: str,
        text_area_width: int,
        font_file_path_name: PathLike,
        first_name: str | None = None,
        last_name: str | None = None,
        maximal_font_size: int = DEFAULT_FONT_MINIMAL_SIZE,
        minimal_font_size: int = DEFAULT_FONT_MAXIMAL_SIZE
) -> tuple[int, int, int, bool]:
    """
    Calculate the optimal font size to display the card owner's full name
    in the specified text area.

    If the text area is too small to write the full name with the minimal
    size of the font, the function calculates the largest size of the font
    that can be used to display the first name and the last name in two
    separated lines.


    :param full_name: A full name of the card owner.

    :param text_area_width: The width in pixels of the area to display the
        full name.

    :param font_file_path_name: The absolute path and name of the font
        file to use to display the full name.

    :param first_name: The first name of the card owner.

    :param last_name: The last name of the card owner.

    :param maximal_font_size: The maximal size of the font to use to
        display the full name.

    :param minimal_font_size: THe minimal size of the font to use to
        display the full name.


    :return: A tuple ``(font_size, text_width, text_height, multiline_required)``
        where:

        - ``font_size: int``: The largest font size to display the text in the
          specified area.

        - ``text_width: int``: The width in pixels of the text displayed with
          this font size.

        - ``text_height: int``: The height in pixels of the text displayed with
          this font size.

        - ``multiline_required: bool``: ``False`` if the full name can be
          displayed on 1 single line; ``True`` if the full name MUST be
          replaced with the first name and the last name on 2 separated lines.
    """
    if not full_name:
        raise ValueError("MUST specify a valid value for argument 'full_name'")

    if text_area_width is None or text_area_width <= 0:
        raise ValueError("MUST specify a valid value for argument 'text_area_width'")

    if minimal_font_size is None or minimal_font_size <= 0:
        raise ValueError("MUST specify a valid value for argument 'minimal_font_size'")

    if maximal_font_size is None or maximal_font_size <= 0:
        raise ValueError("MUST specify a valid value for argument 'maximal_font_size'")

    if minimal_font_size > maximal_font_size:
        raise ValueError("Argument 'minimal_font_size' MUST be lowest than 'maximal_font_size'")

    multiline_required = False
    best_font_size, best_text_width, best_text_height = __calculate_text_optimal_font_size(
        full_name,
        text_area_width,
        font_file_path_name
    )

    if best_text_width > text_area_width:
        if not first_name or not last_name \
           or len(first_name) > len(full_name) \
           or len(last_name) > len(full_name):
            logging.debug(f"- First name: \"{first_name}\"")
            logging.debug(f"- Last name: \"{last_name}\"")
            logging.debug(f"- Full name: \"{full_name}\"")
            raise ValueError("The size of the font is too small compared to the requirement")

        best_first_name_font_size, best_first_name_text_width, best_first_name_text_height = \
            __calculate_text_optimal_font_size(first_name, text_area_width, font_file_path_name)

        best_last_name_font_size, best_last_name_text_width, best_last_name_text_height = \
            __calculate_text_optimal_font_size(last_name, text_area_width, font_file_path_name)

        multiline_required = True
        if best_first_name_font_size < best_last_name_font_size:
            best_font_size, best_text_width, best_text_height = \
                best_first_name_font_size, best_first_name_text_width, best_first_name_text_height
        else:
            best_font_size, best_text_width, best_text_height = \
                best_last_name_font_size, best_last_name_text_width, best_last_name_text_height

    return best_font_size, best_text_width, best_text_height, multiline_required


def __calculate_relative_difference(i: int | float, j: int | float) -> float:
    """
    Calculate the relative difference between two numbers.

    The function takes the absolute difference divided by the absolute
    value of their arithmetic mean.


    :param i: A number.

    :param j: Another number.


    :return: A float representing the relative difference (a ratio) between
        the two numbers passed to this function.
    """
    return 0 if i + j == 0 else abs(i - j) / abs(i + j) * 2


def __calculate_text_optimal_font_size(
        text: str,
        text_area_width: int,
        font_file_path_name: PathLike,
        font_maximal_size: int = DEFAULT_FONT_MAXIMAL_SIZE,
        font_minimal_size: int = DEFAULT_FONT_MINIMAL_SIZE,
        font_size: int = DEFAULT_FONT_SIZE
) -> tuple[int, int, int]:
    """
    Return the optimal font size to render the specified text in the
    given text area.


    :param text: A string to be rendered in one line only.

    :param text_area_width: The width of the area to display the text.

    :param font_file_path_name: The absolute path and name of the font
        file.

    :param font_minimal_size: Minimal acceptable size of the font to
        display the text.

    :param font_maximal_size: Maximal acceptable size of the font to
        display the text.

    :param font_size: The default font size to use.  This size will be
        adjusted to display the text in the largest possible font size.


    :return: A tuple ``(font_size, text_width, text_height)`` where:

        - ``font_size: int``: The largest font size to display the text in the
          specified area.

        - ``text_width: int``: The width in pixels of the text displayed with
          this font size.

        - ``text_height: int``: The height in pixels of the text displayed with
          this font size.
    """
    if not text:
        raise ValueError("MUST specify a valid value for argument 'text'")

    if font_size is None or font_size <= 0:
        raise ValueError("MUST specify a valid value for argument 'font_size'")

    if text_area_width <= 0:
        raise ValueError("MUST specify a valid value for argument 'text_area_width'")

    # Get the size of the bounding of the text when rendered in the given
    # font size.
    font = ImageFont.truetype(str(font_file_path_name), font_size)
    text_width, text_height = __get_text_size(font, text)

    best_font_size, best_text_width, best_text_height = font_size, text_width, text_height

    if text_width > text_area_width:
        # If the rendered text fits within the bounding box, determine the
        # maximum font size to render the text within that bounding box.
        while font_size >= font_minimal_size:
            font_size -= 1
            font = ImageFont.truetype(str(font_file_path_name), font_size)
            text_width, text_height = __get_text_size(font, text)

            if text_width < text_area_width:
                break

            best_font_size, best_text_width, best_text_height = font_size, text_width, text_height

    else:
        # If the rendered text doesn't fit within the bounding box, determine
        # the minimum font size to render the text within that bounding box.
        while font_size <= font_maximal_size:
            font_size += 1
            font = ImageFont.truetype(str(font_file_path_name), font_size)
            text_width, text_height = __get_text_size(font, text)

            if text_width > text_area_width:
                break

            best_font_size, best_text_width, best_text_height = font_size, text_width, text_height

    return best_font_size, best_text_width, best_text_height


def __cleanse_value(value: str) -> str:
    cleansed_value = ''.join([
        c if c.isalnum() else '-'
        for c in value
    ])

    return unidecode.unidecode(cleansed_value)


def __validate_attribute_names(file_name_format: str) -> None:
    """
    Validate the attribute names specified in the format of an ID card
    file name.


    :param file_name_format: A string corresponding to the format of an ID
        card file.


    :raise ValueError: If an attribute name specified in the ID card file
        name format is not supported.
    """
    valid_attribute_names = [
        attribute_name.lower()
        for attribute_name in ID_CARD_FILE_NAME_ATTRIBUTE_NAMES
    ]

    attribute_names = REGEX_ID_CARD_ATTRIBUTE_NAME.findall(file_name_format)
    for attribute_name in attribute_names:
        if attribute_name.lower() not in valid_attribute_names:
            raise ValueError(
                f"Invalid attribute \"{attribute_name}\" specified in the ID card file name format"
            )


def __get_text_size(
        font: FreeTypeFont,
        text: str
) -> tuple[int, int]:
    """
    Return the width and the height in pixels of the bounding box of the
    given text when rendered in the specified font.

    :param font: The font to render the text.

    :param text: The text to render.


    :return: The width and the height in pixels of the bounding box.
    """
    left, top, right, bottom = font.getbbox(text)
    text_width = right - left + 1
    text_height = bottom - top + 1
    return text_width, text_height


def __scale_image(
        header_image: Image,
        view_size: tuple[int, int],
        copy_required: bool = False
) -> Image:
    """
    Scale the header image to a specified size.


    :param header_image: An image to fit withing the specified bounding
        box.

    :param view_size: A tuple ``(width, height)` of the view to display the
        header image in.

    :param copy_required: Indicate whether the function can resize the
        image in place, modifying the ``image`` passed to the function, or
        whether to create a copy of the ``image`` and resize the new image.


    :return: The resized version of the image.
    """
    scaled_header_image = header_image.copy() if copy_required else header_image
    scaled_header_image.thumbnail(view_size)
    return scaled_header_image


def build_card_image_file_name(
        id_card: IdCardInfo,
        file_name_format=None
) -> str:
    """
    Build the name of the ID card's image file.

    An ID card filename format MUST consist of attribute names with which
    to construct that filename.  These attribute names MUST be defined in
    braces.

    For example:

        TLH-{SIS ID}.{Full Name}_{Class Name}


    :note: Duplicate spaces in an attribute value are removed.  Space
        characters are replaced with a hyphen.


    :param id_card: An ID card.

    :param file_name_format: A string corresponding to the format of an ID
        card file.


    :return: The ID card's file name.
    """
    if cast.is_undefined(file_name_format):
        file_name_format = DEFAULT_ID_CARD_FILE_NAME_FORMAT

    __validate_attribute_names(file_name_format)  # Yes, we also validate the default format! :)
    file_name = file_name_format

    # Define the value of each attribute that can be used in the file name
    # format of an ID card.
    attribute_names_values_mapping = {
        family_sheet.DEFAULT_FIELD_NAME_ACCOUNT_SIS_ID: id_card.account_sis_id,
        family_sheet.DEFAULT_FIELD_NAME_CLASS_NAME: id_card.class_name,
        family_sheet.DEFAULT_FIELD_NAME_FIRST_NAME: id_card.first_name,
        family_sheet.DEFAULT_FIELD_NAME_FULL_NAME: id_card.full_name,
        family_sheet.DEFAULT_FIELD_NAME_GRADE_NAME: id_card.grade_name,
        family_sheet.DEFAULT_FIELD_NAME_LAST_NAME: id_card.last_name,
    }

    attribute_names_values_mapping = normalization_utils.normalize_names_codes_mapping(attribute_names_values_mapping)

    # Build the file name by replacing the attribute names with their values.
    attribute_names = set([
        attribute_name.lower()
        for attribute_name in REGEX_ID_CARD_ATTRIBUTE_NAME.findall(file_name_format)
    ])

    for attribute_name in attribute_names:
        attribute_value = __cleanse_value(attribute_names_values_mapping[attribute_name])
        file_name = re.sub(rf'[{{]{attribute_name}[}}]', attribute_value, file_name, flags=re.IGNORECASE)

    return file_name


def calculate_card_image_size(size: str | (int, int)) -> tuple[int, int]:
    """
    Return the image size of an ID card.


    :param size: The desired size of the ID card image.  The specified
        width and height MUST correspond to the ratio of a CR80 standard
        credit card size ID-1 in portrait mode (54mm x 85.6mm).

        This argument is either a tuple of two integers `(width, height)`
        or a string representation of two integers separated with the
        character `x`.  For examples: `(540, 860)` or  `'540x860'`.

        One of the two dimensions, either the width or the height, can be
        omitted.  For examples: ``(540, None)`` or ``'540x'``; ``(None, 860)``,
        or ``'x860'``.

        The function automatically calculates the value of the missing
        dimension.


    :return: A tuple ``(width, height)`` of ID card image.


    :raise ValueError: if the argument ``size_str`` doesn't correspond to 2
        numbers separated with the character ``x``.
    """
    if isinstance(size, str):
        size = size.split('x')
        if len(size) != 2:
            raise ValueError('Invalid image size specification')

    card_image_width, card_image_height = size

    if card_image_width and card_image_height:
        card_image_width = int(card_image_width)
        card_image_height = int(card_image_height)
        if __calculate_relative_difference(
                card_image_width / card_image_height,
                DEFAULT_ID_CARD_RATIO
        ) > DEFAULT_ID_CARD_MAXIMUM_STANDARD_DEVIANCE:
            raise ValueError('invalid ID card image size ratio')
    else:
        if card_image_width is None and card_image_height is None:
            raise ValueError('invalid ID card image size specification')

        if card_image_width:
            card_image_width = int(card_image_width)
            card_image_height = math.ceil(card_image_width / DEFAULT_ID_CARD_RATIO)
        else:
            card_image_height = int(card_image_height)
            card_image_width = math.ceil(card_image_height * DEFAULT_ID_CARD_RATIO)

    return card_image_width, card_image_height


def generate_id_card_image(
        id_card: IdCardInfo,
        card_image_size: tuple[int, int],
        header_image: Image,
        font_name: str,
        font_path: PathLike = None,
        padding: int = 20
):
    """
    Generate an image of an ID card.


    :param id_card: The information about the ID card.

    :param card_image_size: A tuple ``(width, height)`` corresponding to
         the size of the ID card's image to generate.

    :param header_image: The header image to render at the topmost
        position of the card' image.

    :param font_name: The font name to display the full name of the card
        (or their first and last name) on the card image.

    :param font_path: The absolute path of the directory where the font
        files are stored in.

    :param padding: The space in pixels to keep around the card's image.


    :return: The image of the ID card.
    """
    logging.debug(
        f"Generating the ID card image for \"{id_card.full_name}\" "
        f"({id_card.account_sis_id})..."
    )

    # Determine the size of the card image based on the given specification.
    # Create a new object `PIL.Image` with a white background.
    id_card_image = Image.new('RGB', card_image_size, color='white')
    card_image_width, card_image_height = card_image_size

    # Calculate the size of the card's view based on the required padding.
    card_view_width, card_view_height = card_image_width - padding * 2, card_image_height - padding * 2

    # Resize the header image to fit the header view of the ID card, and
    # align and display the resized image to this view.
    header_view_width = card_view_width
    header_view_height = math.ceil((card_image_height - card_view_width - padding * 2) / 2)
    scaled_header_image = __scale_image(header_image, (header_view_width, header_view_height))

    scaled_header_image_width, scaled_header_image_height = scaled_header_image.size
    x = math.ceil((header_view_width - scaled_header_image_width) / 2)
    y = math.ceil((header_view_height - scaled_header_image_height) / 2)
    id_card_image.paste(scaled_header_image, (padding + x, padding + y))

    # Generate the QR code with the card owner's ID and display the QR code
    # image in the center of the ID card.
    qrcode_generator = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )

    qrcode_generator.add_data(id_card.account_sis_id)
    qrcode_generator.make(fit=True)
    qrcode_image = qrcode_generator \
        .make_image(fill_color="black", back_color="white") \
        .resize((card_view_width, card_view_width))

    x = padding
    y = math.ceil((card_image_height - card_view_width) / 2)
    id_card_image.paste(qrcode_image, (x, y))

    # Calculate the optimal font size to display the card owner's full name
    # on one single line (or their first and last names on two separate
    # lines) of the ID card.
    text_area_width = card_view_width

    if font_path is None:
        font_path = Path(LIBRARY_DATA_PATH, DEFAULT_FONT_RELATIVE_PATH)
    font_file_path_name = Path(font_path, f'{font_name}.ttf')

    font_size, text_width, text_height, multiline_required = __calculate_full_name_optimal_font_size(
        id_card.full_name,
        text_area_width,
        font_file_path_name,
        first_name=id_card.first_name,
        last_name=id_card.last_name,
        maximal_font_size=DEFAULT_FONT_MAXIMAL_SIZE,
        minimal_font_size=DEFAULT_FONT_MINIMAL_SIZE
    )

    font = ImageFont.truetype(str(font_file_path_name), font_size)
    image_draw = ImageDraw.Draw(id_card_image)

    y = card_image_height - header_view_height - padding

    if multiline_required:
        x = math.ceil((text_area_width - __get_text_size(font, id_card.first_name)[0]) / 2) + padding
        image_draw.text(
            (x, y),
            id_card.first_name,
            font=font,
            fill='black'
        )

        x = math.ceil((text_area_width - __get_text_size(font, id_card.last_name)[0]) / 2) + padding
        image_draw.text(
            (x, y + DEFAULT_LINE_SPACING + text_height),
            id_card.last_name,
            font=font,
            fill='black'
        )

    else:
        x = math.ceil((text_area_width - text_width) / 2) + padding
        image_draw.text(
            (x, y),
            id_card.full_name,
            font=font,
            fill='black'
        )

    return id_card_image
