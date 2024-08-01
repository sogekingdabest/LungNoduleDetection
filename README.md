# LungNoduleDetection

## Problemas Identificados

1. **Variaciones en la Iluminación**: Algunas imágenes son muy brillantes, mientras que otras son muy oscuras.
2. **Separar los Pulmones**: Necesitamos separar los pulmones y aislar sus contornos.
3. **Detección de Nódulos Cancerosos**: Recopilar nódulos cancerosos dentro del contorno del pulmón, considerando las diferencias de intensidad en la escala de grises.
4. **Excluir Bronquios**: No incluir los bronquios en el contorno pulmonar, teniendo en cuenta su ubicación, forma e intensidad en la escala de grises.

## Solución Implementada

1. **Ecualización de Histograma**: La ecualización del histograma de la imagen se realiza para tener en cuenta las variaciones de iluminación.
2. **Imagen Binaria y Separación de Contornos**: Se crea una imagen binaria y se separan los contornos según el área del conjunto de píxeles que forman los pulmones.
3. **Filtrado para Incluir Nódulos Cancerosos**: El filtrado incluye la mayoría de los nódulos cancerosos en los pulmones.
4. **Cómo Excluir los Bronquios**:
   - **Primer Método**: Utiliza el filtrado descrito en el punto 3.
   - **Segundo Método**:
     1. Crear una imagen binaria para aislar los bronquios.
     2. Filtrar la imagen original ecualizada utilizando el mismo filtro que en el punto 3.
     3. Generar la imagen binaria resultante y agregarla a la imagen binaria del bronquio.
     4. Aplicar una serie de operaciones morfológicas para obtener el resultado final.
