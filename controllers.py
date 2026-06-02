# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import io
import base64

class TrainingMaterialController(http.Controller):

    @http.route('/training/stream/<int:material_id>', type='http', auth='user')
    def stream_training_material(self, material_id, **kwargs):
        """
        Transmite archivos de video, audio y PDF usando el motor nativo de Odoo.
        """
        # Buscamos con sudo() para evitar restricciones de reglas de registro (Record Rules) durante la carga multimedia
        material = request.env['training.material'].sudo().browse(material_id)
        
        if not material.exists() or not material.file:
            return request.not_found()

        try:
            # Odoo guarda los binarios en Base64; el navegador necesita Bytes puros
            file_data = base64.b64decode(material.file)
        except Exception:
            return request.not_found()

        # Envolvemos los bytes decodificados en un flujo de datos legible por Odoo
        file_like = io.BytesIO(file_data)
        filename = material.file_name or 'material_multimedia'

        # Dejar que Odoo maneje las cabeceras de rango, streaming por bloques y tipos MIME de forma nativa
        return request.send_file(
            file_like,
            filename=filename,
            as_attachment=False  # Crucial: 'False' para que se reproduzca en línea y no se autodescargue
        )