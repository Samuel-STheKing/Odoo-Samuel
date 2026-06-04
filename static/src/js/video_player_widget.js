/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, onPatched, useRef, xml } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class VideoPlayerWidget extends Component {
    static props = { ...standardFieldProps };

    static template = xml`
        <div class="o_video_player_widget"
             style="width:100%; background:#000; border-radius:4px; overflow:hidden;">

            <t t-if="props.record.resId and props.record.data.file">
                <video t-ref="videoEl"
                       controls="controls"
                       controlsList="nodownload"
                       preload="metadata"
                       width="100%"
                       height="500"
                       style="display:block; object-fit:contain; background:#000;">
                    El navegador no soporta reproducción de video.
                </video>
            </t>

            <t t-else="">
                <div style="color:#999; text-align:center; padding:80px 20px; min-height:400px;">
                    <i class="fa fa-film fa-3x"
                       style="color:#555; display:block; margin-bottom:12px;"/>
                    <t t-if="!props.record.data.file">
                        <p>Cargue un archivo de video para habilitar el reproductor.</p>
                    </t>
                    <t t-else="">
                        <p style="color:#aaa;">Guarde el registro para reproducir el video.</p>
                    </t>
                </div>
            </t>

        </div>
    `;

    setup() {
        this.videoRef = useRef("videoEl");
        onMounted(() => this._updateSrc());
        onPatched(() => this._updateSrc());
    }

    _updateSrc() {
        const video = this.videoRef.el;
        if (!video) return;

        const recordId = this.props.record.resId;
        const hasFile  = this.props.record.data.file;

        if (recordId && hasFile) {
            const newSrc = `/training/stream/${recordId}`;
            if (video.getAttribute("src") !== newSrc) {
                video.setAttribute("src", newSrc);
                video.load();
            }
        } else {
            video.removeAttribute("src");
            video.load();
        }
    }
}

registry.category("fields").add("video_player", VideoPlayerWidget);