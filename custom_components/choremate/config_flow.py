
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_PERSONS, DEFAULT_PERSONS

class ChoreMateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            persons = [p.strip() for p in user_input["persons_csv"].split(",") if p.strip()]
            lines = int(user_input.get("lines_per_person", 2))
            data = {CONF_PERSONS: [{"name": p, "lines": lines} for p in persons] or DEFAULT_PERSONS}
            return self.async_create_entry(title="ChoreMate", data=data)

        schema = vol.Schema({
            vol.Required("persons_csv", default="Mama,Lina,Alysha"): str,
            vol.Optional("lines_per_person", default=2): int,
        })
        return self.async_show_form(step_id="user", data_schema=schema)
