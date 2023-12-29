import contextvars

sec_user_ctx:contextvars.ContextVar[str] = contextvars.ContextVar('sec_user')
sec_preloaded: contextvars.ContextVar[dict]=contextvars.ContextVar('sec_preloaded')
