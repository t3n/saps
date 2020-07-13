from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


KIND_CHOICES = [
    ("url", "Action URL"),
    ("auto_answer", "Auto Answer"),
    ("blf", "BLF"),
    ("button", "Button"),
    ("call_center_status", "Call Center Status"),
    ("redirect", "Call Forward"),
    ("cancel", "Cancel"),
    ("conference", "Conference"),
    ("F_DISP_CODE", "Disposition Code"),
    ("dtmf", "DTMF"),
    ("dest", "Extension"),
    ("icom", "Intercom"),
    ("ivr", "IVR"),
    ("keyevent", "Key Event"),
    ("line", "Line"),
    ("multicast", "Multicast"),
    ("ok", "OK"),
    ("orbit", "Park"),
    ("presence", "Presence"),
    ("p2t", "Push-to-Talk"),
    ("recorder", "Record"),
    ("smart_transfer", "SmartTransfer"),
    ("speed", "Speed Dial"),
    ("transfer", "Transfer"),
    ("xml", "XML Definition"),
    ("none", "None"),
]


class Phone(models.Model):
    phone_type = models.ForeignKey("PhoneType", on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    device = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    realname = models.CharField(max_length=200, null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.phone_type.phone_type + "-" + self.mac_address


class Firmware(models.Model):
    phone_type = models.ForeignKey("PhoneType", on_delete=models.CASCADE)
    host = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.phone_type.phone_type + "-" + self.host + self.path + self.filename

    def url(self):
        return self.host + self.path + self.filename


class FunctionKey(models.Model):
    phone = models.ForeignKey("Phone", on_delete=models.CASCADE)
    fkey = models.IntegerField()
    kind = models.CharField(
        max_length=20, choices=KIND_CHOICES, default="", null=True, blank=True
    )
    number = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["phone", "fkey"], name="unique_fkey")
        ]

    def __str__(self):
        return (
            self.phone.phone_type.phone_type
            + "-"
            + self.phone.mac_address
            + "-"
            + str(self.fkey)
        )


class Language(models.Model):
    phone_type = models.ForeignKey("PhoneType", on_delete=models.CASCADE)
    host = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.phone_type.phone_type + "-" + self.host + self.path + self.filename

    def url(self):
        return self.host + self.path + self.filename


class PhoneType(models.Model):
    phone_type = models.CharField(max_length=12)
    function_keys = models.IntegerField()

    def __str__(self):
        return self.phone_type


class Setting(models.Model):
    PERM_CHOICES = [
        ("", "None"),
        ("R", "Read"),
        ("RW", "Read/Write"),
    ]
    phone_type = models.ForeignKey(
        "PhoneType", null=True, blank=True, on_delete=models.CASCADE
    )
    phone = models.ForeignKey("Phone", null=True, blank=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    perm = models.CharField(max_length=2, choices=PERM_CHOICES, default="", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["phone_type", "phone", "key"], name="unique_setting"
            )
        ]

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude=exclude)
        try:
            setting = Setting.objects.get(
                phone_type=self.phone_type, phone=self.phone, key=self.key,
            )
            if setting and not setting.pk == self.pk:
                raise ValidationError({NON_FIELD_ERRORS: ["Setting already exists."]})
        except models.ObjectDoesNotExist:
            if self.phone is not None and self.phone_type is not None:
                raise ValidationError(
                    {NON_FIELD_ERRORS: ["Choose phone type or phone not both."]}
                )

    def kind(self):
        kind = "general"
        if self.phone_type:
            kind = self.phone_type.phone_type
        if self.phone:
            kind = self.phone.mac_address

        return kind

    def __str__(self):
        return self.kind() + "-" + self.key + "-" + self.value
