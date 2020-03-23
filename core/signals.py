from core.modbustcp.promodem.client import PromodemClient

CHANGE_FIELDS = ('brightness', 'voltage_inversion', 'threshold_brightness_level', 'brightness_value_when_turned_on',
                 'brightness_step', 'minutes_to_brightness_reset', 'brightness_after_reset')


def change_state(instance):
    if instance.has_changed:
        for field in instance.changed_fields:
            if field in CHANGE_FIELDS:
                client = PromodemClient(host=instance.ip, debug=False)
                func = getattr(client, 'set_' + field)
                if func:
                    result = func(instance.get_field_diff(field)[1])
                    # if not result then start scheduler
                    
# https://stackoverflow.com/questions/1355150/when-saving-how-can-you-check-if-a-field-has-changed
