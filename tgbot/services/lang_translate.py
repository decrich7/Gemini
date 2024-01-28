from tgbot.config import load_config, Config
from tgbot.middlewares.multy_lang import ACLMiddleware



config: Config = load_config()

    # Устанавливаем миддлварь
i18n = ACLMiddleware(config.i18n_data.I18N_DOMAIN, config.i18n_data.LOCALES_DIR)
_ = i18n.gettext
