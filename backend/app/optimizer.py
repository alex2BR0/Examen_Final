from typing import List, Tuple, Dict
from .models import Objeto, OptimizacionResponse
 

class OptimizadorPortafolio:
    """
    Clase que implementa el algoritmo de optimización de portafolio
    utilizando programación dinámica para resolver el problema de la mochila
    """
    
    def __init__(self):
        self.dp_table = None
        self.selected_items = None
    
    def optimizar(self, capacidad: int, objetos: List[Objeto]) -> OptimizacionResponse:
        """
        Optimiza la selección de objetos para maximizar la ganancia
        sin exceder la capacidad dada.
        
        Args:
            capacidad: Capacidad total disponible
            objetos: Lista de objetos disponibles
            
        Returns:
            OptimizacionResponse: Resultado de la optimización
        """
        if not objetos:
            return OptimizacionResponse(
                seleccionados=[],
                ganancia_total=0,
                peso_total=0,
                capacidad_utilizada=0.0,
                eficiencia=0.0
            )
        
        # Convertir objetos a formato de trabajo
        pesos = [obj.peso for obj in objetos]
        ganancias = [obj.ganancia for obj in objetos]
        nombres = [obj.nombre for obj in objetos]
        
        # Resolver usando programación dinámica
        ganancia_maxima, items_seleccionados = self._knapsack_dp(
            capacidad, pesos, ganancias, len(objetos)
        )
        
        # Obtener nombres de objetos seleccionados
        nombres_seleccionados = [nombres[i] for i in items_seleccionados]
        
        # Calcular peso total de la selección
        peso_total = sum(pesos[i] for i in items_seleccionados)
        
        # Calcular métricas adicionales
        capacidad_utilizada = (peso_total / capacidad) * 100 if capacidad > 0 else 0
        eficiencia = ganancia_maxima / peso_total if peso_total > 0 else 0
        
        return OptimizacionResponse(
            seleccionados=nombres_seleccionados,
            ganancia_total=ganancia_maxima,
            peso_total=peso_total,
            capacidad_utilizada=round(capacidad_utilizada, 2),
            eficiencia=round(eficiencia, 4)
        )
    
    def _knapsack_dp(self, capacidad: int, pesos: List[int], 
                     ganancias: List[int], n: int) -> Tuple[int, List[int]]:
        """
        Implementa el algoritmo de programación dinámica para el problema de la mochila.
        
        Args:
            capacidad: Capacidad total de la mochila
            pesos: Lista de pesos de los objetos
            ganancias: Lista de ganancias de los objetos
            n: Número de objetos
            
        Returns:
            Tuple[int, List[int]]: (ganancia máxima, índices de objetos seleccionados)
        """
        # Crear tabla de programación dinámica
        # dp[i][w] = ganancia máxima usando los primeros i objetos con capacidad w
        dp = [[0 for _ in range(capacidad + 1)] for _ in range(n + 1)]
        
        # Llenar la tabla dp
        for i in range(1, n + 1):
            for w in range(capacidad + 1):
                # No incluir el objeto i
                dp[i][w] = dp[i-1][w]
                
                # Incluir el objeto i si es posible
                if pesos[i-1] <= w:
                    dp[i][w] = max(dp[i][w], 
                                 dp[i-1][w - pesos[i-1]] + ganancias[i-1])
        
        # Reconstruir la solución
        items_seleccionados = []
        w = capacidad
        
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                items_seleccionados.append(i-1)
                w -= pesos[i-1]
        
        return dp[n][capacidad], items_seleccionados[::-1]
    
    def obtener_analisis_detallado(self, capacidad: int, objetos: List[Objeto]) -> Dict:
        """
        Proporciona un análisis detallado de la optimización.
        
        Args:
            capacidad: Capacidad total disponible
            objetos: Lista de objetos disponibles
            
        Returns:
            Dict: Análisis detallado incluyendo estadísticas
        """
        resultado = self.optimizar(capacidad, objetos)
        
        # Calcular estadísticas adicionales
        total_objetos = len(objetos)
        objetos_seleccionados = len(resultado.seleccionados)
        ganancia_total_disponible = sum(obj.ganancia for obj in objetos)
        peso_total_disponible = sum(obj.peso for obj in objetos)
        
        # Calcular eficiencia de cada objeto
        eficiencias = []
        for obj in objetos:
            eficiencia = obj.ganancia / obj.peso if obj.peso > 0 else 0
            eficiencias.append({
                'nombre': obj.nombre,
                'eficiencia': round(eficiencia, 4),
                'ganancia': obj.ganancia,
                'peso': obj.peso
            })
        
        # Ordenar por eficiencia descendente
        eficiencias.sort(key=lambda x: x['eficiencia'], reverse=True)
        
        return {
            'resultado_optimizacion': resultado.dict(),
            'estadisticas': {
                'total_objetos_disponibles': total_objetos,
                'objetos_seleccionados': objetos_seleccionados,
                'porcentaje_seleccion': round((objetos_seleccionados / total_objetos) * 100, 2),
                'ganancia_total_disponible': ganancia_total_disponible,
                'ganancia_obtenida': resultado.ganancia_total,
                'porcentaje_ganancia_obtenida': round((resultado.ganancia_total / ganancia_total_disponible) * 100, 2) if ganancia_total_disponible > 0 else 0,
                'peso_total_disponible': peso_total_disponible,
                'peso_utilizado': resultado.peso_total,
                'porcentaje_peso_utilizado': round((resultado.peso_total / peso_total_disponible) * 100, 2) if peso_total_disponible > 0 else 0
            },
            'eficiencias_objetos': eficiencias
        }
