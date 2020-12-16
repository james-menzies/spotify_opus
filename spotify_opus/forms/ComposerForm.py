from wtforms_alchemy import ModelForm

from spotify_opus.models.Composer import Composer


class ComposerForm(ModelForm):
    class Meta:
        model = Composer
        include_primary_keys = False
        exclude = ["image_url"]
