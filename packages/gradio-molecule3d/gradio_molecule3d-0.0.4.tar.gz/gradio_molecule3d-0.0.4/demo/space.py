
import gradio as gr
from app import demo as app
import os

_docs = {'Molecule3D': {'description': 'Creates a file component that allows uploading generic file (when used as an input) and or displaying generic files (output).', 'members': {'__init__': {'value': {'type': 'str | list[str] | Callable | None', 'default': 'None', 'description': 'Default file to display, given as str file path. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'reps': {'type': 'Any | None', 'default': '[]', 'description': None}, 'config': {'type': 'Any | None', 'default': '{\n    "backgroundColor": "white",\n    "orthographic": False,\n    "disableFog": False,\n}', 'description': 'dictionary of config options'}, 'confidenceLabel': {'type': 'str | None', 'default': '"pLDDT"', 'description': 'label for confidence values stored in the bfactor column of a pdb file'}, 'file_count': {'type': '"single" | "multiple" | "directory"', 'default': '"single"', 'description': 'if single, allows user to upload one file. If "multiple", user uploads multiple files. If "directory", user uploads all files in selected directory. Return type will be list for each file in case of "multiple" or "directory".'}, 'file_types': {'type': 'list[str] | None', 'default': 'None', 'description': 'List of file extensions or types of files to be uploaded (e.g. [\'image\', \'.json\', \'.mp4\']). "file" allows any file to be uploaded, "image" allows only image files to be uploaded, "audio" allows only audio files to be uploaded, "video" allows only video files to be uploaded, "text" allows only text files to be uploaded.'}, 'type': {'type': '"filepath" | "binary"', 'default': '"filepath"', 'description': 'Type of value to be returned by component. "file" returns a temporary file object with the same base name as the uploaded file, whose full path can be retrieved by file_obj.name, "binary" returns an bytes object.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. Queue must be enabled. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'height': {'type': 'int | float | None', 'default': 'None', 'description': 'The maximum height of the file component, in pixels. If more files are uploaded than can fit in the height, a scrollbar will appear.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will allow users to upload a file; if False, can only be used to display files. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'showviewer': {'type': 'bool', 'default': 'True', 'description': 'If True, will display the 3Dmol.js viewer. If False, will not display the 3Dmol.js viewer.'}}, 'postprocess': {'value': {'type': 'str | list[str] | None', 'description': "The output data received by the component from the user's function in the backend."}}, 'preprocess': {'return': {'type': 'bytes\n    | gradio.utils.NamedString\n    | list[bytes | gradio.utils.NamedString]\n    | None', 'description': "The preprocessed input data sent to the user's function in the backend."}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the Molecule3D changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the Molecule3D. Uses event data gradio.SelectData to carry `value` referring to the label of the Molecule3D, and `selected` to refer to state of the Molecule3D. See EventData documentation on how to use this event data'}, 'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the Molecule3D using the X button for the component.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the Molecule3D.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'Molecule3D': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_molecule3d`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_molecule3d/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_molecule3d"></a>  
</div>

Molecule3D custom component to visualize pdb or sdf files using 3Dmol.js
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_molecule3d
```

## Usage

```python

import gradio as gr
from gradio_molecule3d import Molecule3D

import os

example = Molecule3D().example_inputs()


reps =    [
    {
      "model": 0,
      "chain": "",
      "resname": "",
      "style": "stick",
      "color": "whiteCarbon",
      "residue_range": "",
      "around": 0,
      "byres": False,
      "visible": False
    }
  ]



def predict(x):
    print("predict function", x)
    print(x.name)
    return x

with gr.Blocks() as demo:
    inp = Molecule3D(label="Molecule3D", reps=reps)
    out = Molecule3D(label="Output", reps=reps)

    btn = gr.Button("Predict")
    gr.Markdown(\"\"\" 
    You can configure the default rendering of the molecule by adding a list of representations
    <pre>
        reps =    [
        {
          "model": 0,
          "chain": "",
          "resname": "",
          "style": "cartoon",
          "color": "whiteCarbon",
          "residue_range": "",
          "around": 0,
          "byres": False,
          "visible": False,
        },
        {
          "model": 0,
          "chain": "A",
          "resname": "HIS",
          "style": "stick",
          "color": "red",
          "residue_range": "",
          "around": 0,
          "byres": False,
          "visible": False,
        }
      ]
    </pre>
    \"\"\")
    btn.click(predict, inputs=inp, outputs=out)


if __name__ == '__main__':
  demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `Molecule3D`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["Molecule3D"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["Molecule3D"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, the preprocessed input data sent to the user's function in the backend.
- **As output:** Should return, the output data received by the component from the user's function in the backend.

 ```python
def predict(
    value: bytes
    | gradio.utils.NamedString
    | list[bytes | gradio.utils.NamedString]
    | None
) -> str | list[str] | None:
    return value
```
""", elem_classes=["md-custom", "Molecule3D-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          Molecule3D: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
