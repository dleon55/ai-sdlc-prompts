# i18n_strings.py
# Diccionario de strings de UI para internacionalización ES/EN
# Fase 1: UI de aplicación principal

UI_STRINGS = {
    'es': {
        # Header
        'app_title': 'AI-SDLC Pro — Biblioteca de Prompts',
        'projects_title': 'Proyectos',
        'projects_tooltip': 'Gestionar proyectos',
        
        # Search bar
        'search_placeholder': 'Buscar por nombre o contenido del prompt...',
        'prompts_count': 'prompts',
        'vars_active': 'Vars activas',
        'multi_select': 'Multi-select',
        'variables': 'Variables',
        
        # Welcome banner
        'welcome_title': 'Bienvenido a AI-SDLC Pro',
        'welcome_pill_1': 'Ciclo SDLC completo: del análisis al incident response',
        'welcome_pill_2': 'Variables de contexto que adaptan cada prompt a tu proyecto',
        'welcome_pill_3': 'Gobernanza multi-agente: Copilot, Claude, Cursor, Windsurf',
        'welcome_dismiss': 'Entendido',
        
        # Project selector
        'project_label': 'Proyecto',
        'change_project_tooltip': 'Cambiar proyecto activo',
        
        # Sidebar
        'sidebar_nav': 'Nav',
        'sidebar_collapse_tooltip': 'Colapsar / expandir menú',
        'section_framework': 'Framework',
        'section_analysis': 'Análisis',
        'section_design': 'Diseño',
        'section_implementation': 'Implementación',
        'section_testing': 'Pruebas',
        'section_deployment': 'Despliegue',
        'section_operations': 'Operaciones',
        
        # Framework banner
        'framework_badge': 'Obligatorio',
        'framework_title': 'PASO 1 — Copia este bloque antes de usar cualquier prompt',
        'framework_desc': 'Este bloque define el rol del agente, el contexto multi-agente y las reglas obligatorias de ingeniería. Sin él, el agente responde de forma genérica. Cópialo y pégalo siempre primero en tu conversación con el agente IA.',
        'framework_copy': 'Copiar framework completo',
        'framework_expand_tooltip': 'Click para expandir/colapsar',
        
        # Card actions
        'card_select_tooltip': 'Seleccionar prompt',
        'card_expand_tooltip': 'Ver / ocultar prompt',
        'card_copy': 'Copiar',
        'card_info_tooltip': 'Cuándo usar · Fórmula de uso estándar',
        
        # Empty state
        'empty_results': 'Sin resultados.',
        'empty_suggestion': 'Intenta con otro término de búsqueda.',
        
        # Variable panel
        'var_panel_title': 'Variables de contexto',
        'var_add_tooltip': 'Añadir nueva variable',
        'var_add_title': 'Nueva variable',
        'var_key_label': 'Clave',
        'var_value_label': 'Valor',
        'var_add_button': 'Añadir',
        'var_cancel': 'Cancelar',
        'var_global': 'Globales',
        'var_per_prompt': 'Por prompt',
        'var_close_tooltip': 'Cerrar panel',
        'var_show_tooltip': 'Panel de variables',
        
        # Info modal
        'info_close_tooltip': 'Cerrar',
        'info_when_use': 'Cuándo usar',
        'info_formula': 'Fórmula de uso',
        
        # Projects modal
        'proj_modal_title': 'Proyectos',
        'proj_new': 'Nuevo proyecto',
        'proj_import': 'Importar',
        'proj_export': 'Exportar seleccionados',
        'proj_export_all': 'Exportar todo',
        'proj_empty': 'Sin prompts seleccionados.',
        'proj_close_tooltip': 'Cerrar',
        'proj_delete_tooltip': 'Eliminar proyecto',
        
        # Language selector
        'language_selector_tooltip': 'Cambiar idioma / Change language',
        'language_es': 'Español',
        'language_en': 'English',
        'language_current': 'Idioma actual',
    },
    'en': {
        # Header
        'app_title': 'AI-SDLC Pro — Prompt Library',
        'projects_title': 'Projects',
        'projects_tooltip': 'Manage projects',
        
        # Search bar
        'search_placeholder': 'Search by prompt name or content...',
        'prompts_count': 'prompts',
        'vars_active': 'Vars active',
        'multi_select': 'Multi-select',
        'variables': 'Variables',
        
        # Welcome banner
        'welcome_title': 'Welcome to AI-SDLC Pro',
        'welcome_pill_1': 'Complete SDLC cycle: from analysis to incident response',
        'welcome_pill_2': 'Context variables that adapt each prompt to your project',
        'welcome_pill_3': 'Multi-agent governance: Copilot, Claude, Cursor, Windsurf',
        'welcome_dismiss': 'Got it',
        
        # Project selector
        'project_label': 'Project',
        'change_project_tooltip': 'Change active project',
        
        # Sidebar
        'sidebar_nav': 'Nav',
        'sidebar_collapse_tooltip': 'Collapse / expand menu',
        'section_framework': 'Framework',
        'section_analysis': 'Analysis',
        'section_design': 'Design',
        'section_implementation': 'Implementation',
        'section_testing': 'Testing',
        'section_deployment': 'Deployment',
        'section_operations': 'Operations',
        
        # Framework banner
        'framework_badge': 'Required',
        'framework_title': 'STEP 1 — Copy this block before using any prompt',
        'framework_desc': 'This block defines the agent role, multi-agent context, and mandatory engineering rules. Without it, the agent responds generically. Copy and paste it always first in your conversation with the AI agent.',
        'framework_copy': 'Copy complete framework',
        'framework_expand_tooltip': 'Click to expand/collapse',
        
        # Card actions
        'card_select_tooltip': 'Select prompt',
        'card_expand_tooltip': 'Show / hide prompt',
        'card_copy': 'Copy',
        'card_info_tooltip': 'When to use · Standard usage formula',
        
        # Empty state
        'empty_results': 'No results.',
        'empty_suggestion': 'Try another search term.',
        
        # Variable panel
        'var_panel_title': 'Context variables',
        'var_add_tooltip': 'Add new variable',
        'var_add_title': 'New variable',
        'var_key_label': 'Key',
        'var_value_label': 'Value',
        'var_add_button': 'Add',
        'var_cancel': 'Cancel',
        'var_global': 'Global',
        'var_per_prompt': 'Per prompt',
        'var_close_tooltip': 'Close panel',
        'var_show_tooltip': 'Variables panel',
        
        # Info modal
        'info_close_tooltip': 'Close',
        'info_when_use': 'When to use',
        'info_formula': 'Usage formula',
        
        # Projects modal
        'proj_modal_title': 'Projects',
        'proj_new': 'New project',
        'proj_import': 'Import',
        'proj_export': 'Export selected',
        'proj_export_all': 'Export all',
        'proj_empty': 'No prompts selected.',
        'proj_close_tooltip': 'Close',
        'proj_delete_tooltip': 'Delete project',
        
        # Language selector
        'language_selector_tooltip': 'Cambiar idioma / Change language',
        'language_es': 'Español',
        'language_en': 'English',
        'language_current': 'Current language',
    }
}

# Sección labels para sidebar (mapeo dinámico)
SECTION_LABELS_I18N = {
    'es': {
        '00': 'Framework',
        '01': 'Comprensión',
        '02': 'Análisis',
        '03': 'Análisis Técnico',
        '04': 'Diseño',
        '05': 'Planificación',
        '06': 'Implementación',
        '07': 'Pruebas',
        '08': 'Revisión',
        '09': 'Integración',
        '10': 'Documentación',
        '11': 'Operaciones',
        '12': 'Orquestador',
    },
    'en': {
        '00': 'Framework',
        '01': 'Comprehension',
        '02': 'Analysis',
        '03': 'Technical Analysis',
        '04': 'Design',
        '05': 'Planning',
        '06': 'Implementation',
        '07': 'Testing',
        '08': 'Review',
        '09': 'Integration',
        '10': 'Documentation',
        '11': 'Operations',
        '12': 'Orchestrator',
    }
}

# Idiomas soportados
SUPPORTED_LANGUAGES = ['es', 'en']
DEFAULT_LANGUAGE = 'es'

def get_string(key: str, lang: str = 'es') -> str:
    """
    Obtiene un string de UI traducido.
    
    Args:
        key: Clave del string en UI_STRINGS
        lang: Código de idioma ('es' o 'en')
    
    Returns:
        String traducido, o clave si no se encuentra
    """
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    
    return UI_STRINGS.get(lang, UI_STRINGS[DEFAULT_LANGUAGE]).get(key, key)

def get_section_label(section_key: str, lang: str = 'es') -> str:
    """
    Obtiene el label traducido de una sección.
    
    Args:
        section_key: Código de sección (ej: '01', '02')
        lang: Código de idioma
    
    Returns:
        Label traducido de la sección
    """
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    
    return SECTION_LABELS_I18N.get(lang, SECTION_LABELS_I18N[DEFAULT_LANGUAGE]).get(section_key, section_key)

def detect_language() -> str:
    """
    Detecta el idioma preferido basado en navigator.language.
    Solo se usa en runtime (JavaScript), aquí como referencia.
    
    Returns:
        Código de idioma ('es' o 'en')
    """
    # Esta función es documentación del algoritmo;
    # la implementación real está en JavaScript en build.py
    return DEFAULT_LANGUAGE
