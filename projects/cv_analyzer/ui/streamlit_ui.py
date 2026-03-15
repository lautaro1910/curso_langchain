import streamlit as st
from models.cv_model import AnalyzeCV
from services.pdf_processor import extract_text_from_pdf
from services.cv_evaluator import evaluar_candidato
from ui.locales import TRANSLATIONS
import time

# Try to look for fpdf to enable/disable feature
try:
    from services.report_generator import generate_pdf_report
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

def main():
    """Función principal que define la interfaz de usuario de Streamlit"""
    
    st.set_page_config(
        page_title="CV Analyzer IA",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Language Selector in Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        lang_option = st.selectbox(
            "Language / Idioma",
            options=["Español", "English"],
            index=0
        )
        lang_code = "es" if lang_option == "Español" else "en"
        st.session_state['lang_code'] = lang_code
    
    t = TRANSLATIONS[lang_code]

    with st.sidebar:
        # Profile Selector
        st.markdown("---")
        profile_options = {
            "it": t["opt_it"],
            "marketing": t["opt_marketing"]
        }
        
        # Reverse mapping for display
        display_options = list(profile_options.values())
        
        selected_display = st.selectbox(
            t["lbl_profile_type"],
            options=display_options,
            index=0
        )
        
        # Get key from value
        selected_profile = next(key for key, value in profile_options.items() if value == selected_display)
        st.session_state['profile_type'] = selected_profile

    # Main Layout
    st.title(t["main_title"])
    st.markdown(t["description"])
    
    st.divider()
    
    col_entrada, col_resultado = st.columns([1, 1.2], gap="large")
    
    with col_entrada:
        procesar_entrada(t)
    
    with col_resultado:
        mostrar_area_resultados(t, lang_code)

def procesar_entrada(t):
    """Maneja la entrada de datos del usuario"""
    
    st.subheader(t["input_header"])
    
    archivo_cv = st.file_uploader(
        t["upload_label"],
        type=['pdf'],
        help=t["upload_help"]
    )
    
    if archivo_cv is not None:
        st.success(t["file_uploaded"].format(name=archivo_cv.name))
        # st.caption(t["file_size"].format(size=archivo_cv.size)) 
    
    st.markdown("---")
    
    st.markdown(t["job_desc_header"])
    descripcion_puesto = st.text_area(
        t["job_desc_label"],
        height=300,
        placeholder=t["job_desc_placeholder"],
        help=t["job_desc_help"]
    )
    
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        analizar = st.button(
            t["btn_analyze"], 
            type="primary",
            use_container_width=True
        )
    
    with col_btn2:
        if st.button(t["btn_clear"], use_container_width=True):
            st.rerun()
    
    # Store in session state
    if analizar:
        st.session_state['trigger_analyze'] = True
    
    st.session_state['archivo_cv'] = archivo_cv
    st.session_state['descripcion_puesto'] = descripcion_puesto

def mostrar_area_resultados(t, lang_code):
    """Muestra el área de resultados del análisis"""
    
    st.subheader(t["results_header"])
    
    if st.session_state.get('trigger_analyze', False):
        archivo_cv = st.session_state.get('archivo_cv')
        descripcion_puesto = st.session_state.get('descripcion_puesto', '').strip()
        
        if archivo_cv is None:
            st.error(t["error_no_cv"])
            st.session_state['trigger_analyze'] = False
            return
            
        if not descripcion_puesto:
            st.error(t["error_no_desc"])
            st.session_state['trigger_analyze'] = False
            return
        
        procesar_analisis(archivo_cv, descripcion_puesto, t, lang_code)
    else:
        st.info(t["instructions_info"])

def procesar_analisis(archivo_cv, descripcion_puesto, t, lang_code):
    """Procesa el análisis completo del CV"""
    
    # Create a container for the status to keep it clean
    status_container = st.status(t["processing_spinner"], expanded=True)
    
    with status_container:
        st.write(t["step_extract"])
        texto_cv = extract_text_from_pdf(archivo_cv)
        
        if texto_cv.startswith("Error"):
            status_container.update(label="Error", state="error")
            st.error(f"❌ {texto_cv}")
            return
        
        st.write(t["step_prepare"])
        # Artificial delay for UX if it's too fast, or just to show steps
        # time.sleep(0.5) 
        
        st.write(t["step_analyze"])
        profile_type = st.session_state.get('profile_type', 'it')
        resultado = evaluar_candidato(texto_cv, descripcion_puesto, profile_type)
        
        status_container.update(label=t["step_done"], state="complete", expanded=False)
        
    mostrar_resultados(resultado, t, lang_code)

def mostrar_resultados(result: AnalyzeCV, t, lang_code):
    """Muestra los resultados del análisis de manera estructurada y profesional"""
    
    # Metrics row
    col1, col2 = st.columns([1, 2])
    
    with col1:
        score = result.percentage_match
        if score >= 80:
            color = "normal" # Default green-ish in stats usually, but let's use delta
            delta_color = "normal"
            nivel = t["eval_excellent"]
        elif score >= 60:
            delta_color = "off" # Gray/Yellowish
            nivel = t["eval_good"]
        elif score >= 40:
            delta_color = "inverse" # Red/Orange
            nivel = t["eval_regular"]
        else:
            delta_color = "inverse"
            nivel = t["eval_low"]
            
        st.metric(
            label=t["eval_match"],
            value=f"{score}%",
            delta=nivel,
            delta_color="normal" if score >= 60 else "inverse"
        )
    
    with col2:
        if score >= 80:
            st.success(f"**{t['msg_excellent']}**")
        elif score >= 60:
            st.warning(f"**{t['msg_good']}**")
        elif score >= 40:
            st.info(f"**{t['msg_regular']}**")
        else:
            st.error(f"**{t['msg_low']}**")

    st.markdown("---")
    
    # Profile & Experience
    st.subheader(t["profile_header"])
    p_col1, p_col2 = st.columns(2)
    p_col1.markdown(f"**{t['lbl_name']}** {result.name_candidate}")
    p_col1.markdown(f"**{t['lbl_exp']}** {result.years_of_experience} {t['years']}")
    p_col2.markdown(f"**{t['lbl_edu']}** {', '.join(result.education)}")
    
    with st.expander(t["exp_header"], expanded=True):
        if isinstance(result.experience, list):
            for exp in result.experience:
                st.markdown(f"- {exp}")
        else:
            st.write(result.experience)

    # Skills & Strengths grid
    st.markdown("#### " + t["skills_header"])
    if result.abilities:
        # Badge style
        st.markdown(" ".join([f"`{skill}`" for skill in result.abilities]))
    else:
        st.caption(t["no_skills"])
    
    st.markdown("---")
    
    c_str, c_area = st.columns(2)
    
    with c_str:
        st.markdown("#### " + t["strengths_header"])
        if result.strengths:
            for s in result.strengths:
                st.markdown(f"- {s}")
        else:
            st.caption(t["no_strengths"])
            
    with c_area:
        st.markdown("#### " + t["areas_header"])
        if result.areas_for_improvement:
            for a in result.areas_for_improvement:
                st.markdown(f"- {a}")
        else:
            st.caption(t["no_areas"])

    st.markdown("---")
    
    # Download Section
    if PDF_AVAILABLE:
        try:
            pdf_bytes = generate_pdf_report(result, lang_code, TRANSLATIONS)
            st.download_button(
                label=t["btn_download"],
                data=pdf_bytes,
                file_name=t["download_filename"],
                mime='application/pdf',
                type="primary",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
    else:
        st.warning("PDF generation is unavailable (fpdf not installed).")