# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64
import re


class TrainingMaterialController(http.Controller):

    @http.route('/training/stream/<int:material_id>', type='http', auth='user')
    def stream_training_material(self, material_id, **kwargs):
        material = request.env['training.material'].sudo().browse(material_id)

        if not material.exists() or not material.file:
            return request.not_found()

        try:
            file_data = base64.b64decode(material.file)
        except Exception:
            return request.not_found()

        total_length = len(file_data)
        filename = material.file_name or 'video.mp4'

        # Detectar Content-Type
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        mime_map = {
            'mp4':  'video/mp4',
            'webm': 'video/webm',
            'ogv':  'video/ogg',
            'ogg':  'video/ogg',
            'mov':  'video/quicktime',
            'mp3':  'audio/mpeg',
            'wav':  'audio/wav',
            'm4a':  'audio/mp4',
        }
        content_type = mime_map.get(ext, 'application/octet-stream')

        # Leer el header Range del request
        range_header = request.httprequest.headers.get('Range', None)

        if range_header:
            # Parsear "bytes=start-end"
            match = re.match(r'bytes=(\d+)-(\d*)', range_header)
            if match:
                start = int(match.group(1))
                end   = int(match.group(2)) if match.group(2) else total_length - 1

                # Validar rango
                end = min(end, total_length - 1)
                chunk = file_data[start:end + 1]
                chunk_length = len(chunk)

                headers = [
                    ('Content-Type',   content_type),
                    ('Content-Length', chunk_length),
                    ('Content-Range',  f'bytes {start}-{end}/{total_length}'),
                    ('Accept-Ranges',  'bytes'),
                    ('Cache-Control',  'no-store'),
                ]
                # 206 Partial Content — clave para que el navegador reproduzca
                response = request.make_response(chunk, headers=headers)
                response.status_code = 206
                return response

        # Sin Range header → respuesta completa normal
        headers = [
            ('Content-Type',   content_type),
            ('Content-Length', total_length),
            ('Accept-Ranges',  'bytes'),   # avisa al navegador que soportamos Range
            ('Cache-Control',  'no-store'),
        ]
        return request.make_response(file_data, headers=headers)