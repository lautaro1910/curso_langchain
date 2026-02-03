from pydantic import BaseModel, Field

# Modelo de datos para analizar un CV y obtener información relevante
class AnalyzeCV(BaseModel):
    name_candidate: str = Field(description="Nombre del candidato")
    years_of_experience: int = Field(description="Años de experiencia laboral relevantes")
    abilities: list[str] = Field(description="Habilidades clave más relevantes (5-7 habilidades)")
    education: list[str] = Field(description="Nivel educativo más alto y especialización principal")
    experience: list[str] = Field(description="Resumen conciso de la experiencia laboral relevante")
    strengths: list[str] = Field(description="Fortalezas clave del candidato")
    areas_for_improvement: list[str] = Field(description="Áreas donde el candidato puede mejorar (2-3 áreas)")
    percentage_match: int = Field(description="Porcentaje de coincidencia con el perfil (0-100) basado en experiencia, habilidades y educación", ge=0, le=100)


