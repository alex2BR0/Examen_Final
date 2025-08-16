import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Objeto, OptimizacionRequest, OptimizacionResponse
from app.optimizer import OptimizadorPortafolio



class TestOptimizadorPortafolio:
    """Clase de pruebas para el optimizador de portafolio"""
    
    def setup_method(self):
        """Configuración inicial para cada prueba"""
        self.optimizador = OptimizadorPortafolio()
    
    def test_caso_exito_1_maximo_aprovechamiento(self):
        """Prueba el caso de éxito 1: máximo aprovechamiento de capacidad"""
        capacidad = 10000
        objetos = [
            Objeto(nombre="Fondo_A", peso=2000, ganancia=1500),
            Objeto(nombre="Fondo_B", peso=4000, ganancia=3500),
            Objeto(nombre="Fondo_C", peso=5000, ganancia=4000),
            Objeto(nombre="Fondo_D", peso=3000, ganancia=2500),
            Objeto(nombre="Fondo_E", peso=1500, ganancia=1800)
        ]
        
        resultado = self.optimizador.optimizar(capacidad, objetos)
        
        # Verificar que la ganancia total sea 9300 (Fondo_B + Fondo_C + Fondo_E)
        assert resultado.ganancia_total == 9300
        assert resultado.peso_total == 10000
        assert resultado.capacidad_utilizada == 100.0
        assert set(resultado.seleccionados) == {"Fondo_B", "Fondo_C", "Fondo_E"}
    
    def test_caso_exito_2_capacidad_limitada(self):
        """Prueba el caso de éxito 2: capacidad limitada"""
        capacidad = 8000
        objetos = [
            Objeto(nombre="Acción_X", peso=1000, ganancia=800),
            Objeto(nombre="Acción_Y", peso=2500, ganancia=2200),
            Objeto(nombre="Acción_Z", peso=3000, ganancia=2800),
            Objeto(nombre="Bono_P", peso=4000, ganancia=3000),
            Objeto(nombre="Bono_Q", peso=1500, ganancia=1200)
        ]
        
        resultado = self.optimizador.optimizar(capacidad, objetos)
        
        # Verificar que no exceda la capacidad
        assert resultado.peso_total <= capacidad
        assert resultado.capacidad_utilizada <= 100.0
        assert len(resultado.seleccionados) > 0
    
    def test_caso_exito_3_proyectos_bajo_costo(self):
        """Prueba el caso de éxito 3: proyectos de bajo costo, alta rentabilidad"""
        capacidad = 5000
        objetos = [
            Objeto(nombre="Cripto_1", peso=500, ganancia=700),
            Objeto(nombre="Cripto_2", peso=800, ganancia=1000),
            Objeto(nombre="ETF_1", peso=1500, ganancia=1300),
            Objeto(nombre="ETF_2", peso=2000, ganancia=1800),
            Objeto(nombre="NFT_Alpha", peso=3000, ganancia=2500)
        ]
        
        resultado = self.optimizador.optimizar(capacidad, objetos)
        
        # Verificar que no exceda la capacidad
        assert resultado.peso_total <= capacidad
        assert resultado.ganancia_total > 0
    
    def test_caso_limite_capacidad_cero(self):
        """Prueba caso límite: capacidad cero"""
        capacidad = 0
        objetos = [
            Objeto(nombre="Test", peso=100, ganancia=50)
        ]
        
        resultado = self.optimizador.optimizar(capacidad, objetos)
        
        assert resultado.ganancia_total == 0
        assert resultado.peso_total == 0
        assert len(resultado.seleccionados) == 0
        assert resultado.capacidad_utilizada == 0.0
    
    def test_caso_limite_objetos_vacios(self):
        """Prueba caso límite: lista de objetos vacía"""
        capacidad = 1000
        objetos = []
        
        resultado = self.optimizador.optimizar(capacidad, objetos)
        
        assert resultado.ganancia_total == 0
        assert resultado.peso_total == 0
        assert len(resultado.seleccionados) == 0
        assert resultado.capacidad_utilizada == 0.0
    
    def test_caso_limite_un_solo_objeto(self):
        """Prueba caso límite: un solo objeto"""
        capacidad = 1000
        objetos = [Objeto(nombre="Solo", peso=500, ganancia=300)]
        
        resultado = self.optimizador.optimizar(capacidad, objetos)
        
        assert resultado.ganancia_total == 300
        assert resultado.peso_total == 500
        assert resultado.seleccionados == ["Solo"]
        assert resultado.capacidad_utilizada == 50.0
    
    def test_caso_limite_objeto_excede_capacidad(self):
        """Prueba caso límite: objeto que excede la capacidad"""
        capacidad = 100
        objetos = [
            Objeto(nombre="Grande", peso=200, ganancia=1000),
            Objeto(nombre="Pequeño", peso=50, ganancia=100)
        ]
        
        resultado = self.optimizador.optimizar(capacidad, objetos)
        
        # Debe seleccionar solo el objeto pequeño
        assert resultado.ganancia_total == 100
        assert resultado.peso_total == 50
        assert resultado.seleccionados == ["Pequeño"]
    
    def test_caso_limite_pesos_iguales(self):
        """Prueba caso límite: objetos con pesos iguales"""
        capacidad = 200
        objetos = [
            Objeto(nombre="A", peso=100, ganancia=50),
            Objeto(nombre="B", peso=100, ganancia=60),
            Objeto(nombre="C", peso=100, ganancia=40)
        ]
        
        resultado = self.optimizador.optimizar(capacidad, objetos)
        
        # Debe seleccionar A y B (mayor ganancia total)
        assert resultado.ganancia_total == 110
        assert resultado.peso_total == 200
        assert set(resultado.seleccionados) == {"A", "B"}
    
    def test_caso_limite_ganancias_iguales(self):
        """Prueba caso límite: objetos con ganancias iguales"""
        capacidad = 200
        objetos = [
            Objeto(nombre="A", peso=100, ganancia=50),
            Objeto(nombre="B", peso=80, ganancia=50),
            Objeto(nombre="C", peso=120, ganancia=50)
        ]
        
        resultado = self.optimizador.optimizar(capacidad, objetos)
        
        # Debe seleccionar A y B (menor peso total)
        assert resultado.ganancia_total == 100
        assert resultado.peso_total == 180
        assert set(resultado.seleccionados) == {"A", "B"}
    
    def test_analisis_detallado(self):
        """Prueba el análisis detallado"""
        capacidad = 1000
        objetos = [
            Objeto(nombre="A", peso=300, ganancia=200),
            Objeto(nombre="B", peso=400, ganancia=300),
            Objeto(nombre="C", peso=500, ganancia=400)
        ]
        
        analisis = self.optimizador.obtener_analisis_detallado(capacidad, objetos)
        
        # Verificar estructura del análisis
        assert 'resultado_optimizacion' in analisis
        assert 'estadisticas' in analisis
        assert 'eficiencias_objetos' in analisis
        
        # Verificar estadísticas
        stats = analisis['estadisticas']
        assert stats['total_objetos_disponibles'] == 3
        assert stats['ganancia_total_disponible'] == 900
        assert stats['peso_total_disponible'] == 1200
        
        # Verificar eficiencias
        eficiencias = analisis['eficiencias_objetos']
        assert len(eficiencias) == 3
        # Debe estar ordenado por eficiencia descendente
        assert eficiencias[0]['eficiencia'] >= eficiencias[1]['eficiencia']
        assert eficiencias[1]['eficiencia'] >= eficiencias[2]['eficiencia']


class TestModelos:
    """Clase de pruebas para los modelos Pydantic"""
    
    def test_objeto_valido(self):
        """Prueba creación de objeto válido"""
        objeto = Objeto(nombre="Test", peso=100, ganancia=50)
        assert objeto.nombre == "Test"
        assert objeto.peso == 100
        assert objeto.ganancia == 50
    
    def test_objeto_nombre_vacio(self):
        """Prueba validación de nombre vacío"""
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            Objeto(nombre="", peso=100, ganancia=50)
    
    def test_objeto_peso_negativo(self):
        """Prueba validación de peso negativo"""
        with pytest.raises(ValueError, match="El peso debe ser mayor que 0"):
            Objeto(nombre="Test", peso=-100, ganancia=50)
    
    def test_objeto_ganancia_negativa(self):
        """Prueba validación de ganancia negativa"""
        with pytest.raises(ValueError, match="La ganancia no puede ser negativa"):
            Objeto(nombre="Test", peso=100, ganancia=-50)
    
    def test_optimizacion_request_valido(self):
        """Prueba creación de request válido"""
        objetos = [Objeto(nombre="Test", peso=100, ganancia=50)]
        request = OptimizacionRequest(capacidad=1000, objetos=objetos)
        assert request.capacidad == 1000
        assert len(request.objetos) == 1
    
    def test_optimizacion_request_capacidad_negativa(self):
        """Prueba validación de capacidad negativa"""
        objetos = [Objeto(nombre="Test", peso=100, ganancia=50)]
        with pytest.raises(ValueError, match="La capacidad debe ser mayor que 0"):
            OptimizacionRequest(capacidad=-1000, objetos=objetos)
    
    def test_optimizacion_request_objetos_duplicados(self):
        """Prueba validación de nombres duplicados"""
        objetos = [
            Objeto(nombre="Test", peso=100, ganancia=50),
            Objeto(nombre="Test", peso=200, ganancia=100)
        ]
        with pytest.raises(ValueError, match="Los nombres de los objetos deben ser únicos"):
            OptimizacionRequest(capacidad=1000, objetos=objetos)


if __name__ == "__main__":
    pytest.main([__file__])
