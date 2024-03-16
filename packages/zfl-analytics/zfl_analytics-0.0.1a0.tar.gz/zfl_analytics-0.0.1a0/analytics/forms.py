from django import forms  # type: ignore

from .models import AnalyticsAppSettings


class AnalyticsAppSettingsForm(forms.ModelForm):
    class Meta:
        model = AnalyticsAppSettings
        fields = "__all__"

    def clean(self):
        col_sum = (
            self.cleaned_data["col_left"]
            + self.cleaned_data["col_center"]
            + self.cleaned_data["col_right"]
        )
        maxmum_col_val = 12
        if not col_sum <= maxmum_col_val:
            error_text = f"「レイアウト調整」のカラム総数が{col_sum}です。\n12に合わせる必要があります。"
            raise forms.ValidationError(error_text)

        return self.cleaned_data
