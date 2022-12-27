import time


class AddObject:

    @staticmethod
    def add_text_autocad(text, position, rotation, height, model, text_styles, alignment):
        """
        Создает простой текст в AutoCAD
        """
        try:
            new_text = model.AddText(text, position, height)
            new_text.Rotation = rotation
            new_text.StyleName = text_styles
            new_text.Alignment = alignment
            if alignment != 0:
                new_text.TextAlignmentPoint = position
        except AttributeError:
            new_text = model.AddText(text, position, height)
            new_text.Rotation = rotation
            new_text.StyleName = text_styles
            new_text.Alignment = alignment
            new_text.TextAlignmentPoint = position
