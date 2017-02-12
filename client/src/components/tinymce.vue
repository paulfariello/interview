<template>
	<textarea v-model="value"></textarea>
</template>

<script>
import tinymce from 'tinymce'
import 'tinymce/themes/modern/theme'
import 'tinymce/skins/lightgray/content.min.css'
import 'tinymce/skins/lightgray/skin.min.css'

export default {
	name: 'tinymce',
	props: ['value'],
	watch: {
		'value': function () {
			if (this.$el.value !== this.value) {
				this.editor.setContent(this.value)
			}
		}
	},
	mounted: function () {
		var self = this
		tinymce.init({
			target: this.$el,
			skin: false,
			init_instance_callback: function (editor) {
				self.editor = editor
				editor.on('change', function (e) {
					console.trace()
					editor.save()
					self.$emit('input', self.$el.value)
				})
			}
		})
	}
}
</script>
