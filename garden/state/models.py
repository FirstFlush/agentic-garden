from peewee import (
    AutoField,
    TextField,
    DateTimeField,
    BooleanField,
    FloatField,
)
from ..db.base import StateModel


class LightState(StateModel):

    id = AutoField()
    sensor_id = TextField()
    is_light_on = BooleanField()
    intensity = FloatField()              # normalized 0–1
    state_started_at = DateTimeField(index=True)

    class Meta: # type: ignore[misc]
        table_name = "light_state"


class ClimateState(StateModel):
    id = AutoField()
    sensor_id = TextField()

    temperature_c = FloatField()
    humidity_rh = FloatField()
    vpd_kpa = FloatField(null=True)

    temperature_level = TextField()   # TemperatureLevel
    temperature_trend = TextField()   # TemperatureTrend

    humidity_level = TextField()      # HumidityLevel
    humidity_trend = TextField()      # HumidityTrend

    state_started_at = DateTimeField(index=True)

    class Meta: # type: ignore[misc]
        table_name = "climate_state"


class SoilMoistureState(StateModel):
    id = AutoField()
    sensor_id = TextField()
    avg_moisture = FloatField()           # normalized 0–1
    level = TextField()                   # enum value
    trend = TextField()                   # enum value
    state_started_at = DateTimeField(index=True)

    class Meta: # type: ignore[misc]
        table_name = "soil_moisture_state"