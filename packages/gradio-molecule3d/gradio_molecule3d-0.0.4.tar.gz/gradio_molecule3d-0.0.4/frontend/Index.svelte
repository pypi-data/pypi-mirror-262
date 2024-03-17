<svelte:options accessors={true} />

<script context="module" lang="ts">
  export { default as FilePreview } from "./shared/FilePreview.svelte";
  export { default as BaseFileUpload } from "./shared/FileUpload.svelte";
  export { default as BaseFile } from "./shared/File.svelte";
  export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
  import type { Gradio, SelectData } from "@gradio/utils";
  import File from "./shared/File.svelte";
  import FileUpload from "./shared/FileUpload.svelte";
  import { type FileData } from "@gradio/client";
  import { Block, UploadText } from "@gradio/atoms";
  import { StatusTracker } from "@gradio/statustracker";
  import type { LoadingStatus } from "@gradio/statustracker";
  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;
  export let value: null | FileData | FileData[];
  export let interactive: boolean;
  export let root: string;
  export let label: string;
  export let show_label: boolean;
  export let height: number | undefined = undefined;
  //Molecule3D specific arguments
  export let reps: any = [];
  export let config: any = {};
  export let confidenceLabel: string = "";
  export let showviewer: boolean = true;
  export let _selectable = false;
  export let loading_status: LoadingStatus;
  export let container = true;
  export let scale: number | null = null;
  export let min_width: number | undefined = undefined;
  export let gradio: Gradio<{
    change: never;
    error: string;
    upload: never;
    clear: never;
    select: SelectData;
  }>;
  export let file_count: string;
  export let file_types: string[] = ["file"];
  let old_value = value;
  $: if (JSON.stringify(old_value) !== JSON.stringify(value)) {
    gradio.dispatch("change");
    old_value = value;
    console.log("value change", value);
    moldata = null;
    retrieveContent(value);
  }
  let dragging = false;
  let pending_upload = false;
  //check for missing keys in reps
  let keys_for_reps = {
    model: {
      type: Number,
      default: 0,
    },
    chain: {
      type: String,
      default: "",
    },
    resname: {
      type: String,
      default: "",
    },
    style: {
      type: String,
      default: "cartoon",
      choices: ["cartoon", "stick", "sphere", "surface"],
    },
    color: {
      type: String,
      default: "whiteCarbon",
      choices: [
        "whiteCarbon",
        "orangeCarbon",
        "redCarbon",
        "blackCarbon",
        "blueCarbon",
        "grayCarbon",
        "greenCarbon",
        "cyanCarbon",
        "alphafold",
        "default",
        "Jmol",
        "chain",
        "spectrum",
      ],
    },
    residue_range: {
      type: String,
      default: "",
    },
    around: {
      type: Number,
      default: 0,
    },
    byres: {
      type: Boolean,
      default: false,
    },
    visible: {
      type: Boolean,
      default: true,
    },
  };
  let moldata = null;
  let allowed_extensions = ["pdb", "sdf", "mol2", "pdb1"];
  async function fetchFileContent(url) {
    const response = await fetch(url);
    const content = await response.text();
    return content;
  }
  let promise = null;
  let errors = [];
  async function retrieveContent(value) {
    if (value == null) {
      return [];
    } else if (Array.isArray(value)) {
      let tempMoldata = [];
      // get file extension
      for (const element of value) {
        let ext = element.orig_name.split(".").pop();
        if (!allowed_extensions.includes(ext)) {
          errors.push(
            `Invalid file extension for ${
              element.orig_name
            }. Expected one of ${allowed_extensions.join(", ")}, got ${ext}`
          );
          moldata = null;
          continue;
        }
        tempMoldata.push({
          data: await fetchFileContent(element.url),
          name: element.orig_name,
          format: ext,
          asFrames: false,
        });
      }
      moldata = tempMoldata;
    } else if (typeof value === "object" && value !== null) {
      let ext = value.orig_name.split(".").pop();
      if (!allowed_extensions.includes(ext)) {
        errors.push(
          `Invalid file extension for ${
            value.orig_name
          }. Expected one of ${allowed_extensions.join(", ")}, got ${ext}`
        );
        moldata = null;
      } else {
        let t = await fetchFileContent(value.url);
        let ext = value.orig_name.split(".").pop();
        if (ext === "pdb1") {
          ext = "pdb";
        }
        moldata = [
          { data: t, name: value.orig_name, format: ext, asFrames: false },
        ];
      }
    } else {
      moldata = null;
    }
    // value is object
  }
  // go through each rep, do a type check and add missing keys to the rep
  let lenMoldata = 0;
  $: lenMoldata = moldata ? moldata.length : 0;
  let representations = [];
  //first add all missing keys
  $: {
    reps.forEach((rep) => {
      for (const [key, value] of Object.entries(keys_for_reps)) {
        if (rep[key] === undefined) {
          rep[key] = value["default"];
        }
        if (rep[key].constructor != value["type"]) {
          errors.push(
            `Invalid type for ${key} in reps. Expected ${
              value["type"]
            }, got ${typeof rep[key]}`
          );
        }
      }
    });
    // then check if model does exist and add to representations
    reps.forEach((rep) => {
      if (rep["model"] <= lenMoldata) {
        representations.push(rep);
      }
    });
  }
  $: promise = retrieveContent(value);
</script>

<Block
  {visible}
  variant={value === null ? "dashed" : "solid"}
  border_mode={dragging ? "focus" : "base"}
  padding={false}
  {elem_id}
  {elem_classes}
  {container}
  {scale}
  {min_width}
  allow_overflow={false}
>
  <StatusTracker
    autoscroll={gradio.autoscroll}
    i18n={gradio.i18n}
    {...loading_status}
    status={pending_upload
      ? "generating"
      : loading_status?.status || "complete"}
  />

  {#if !interactive}
    <File
      on:select={({ detail }) => gradio.dispatch("select", detail)}
      selectable={_selectable}
      {value}
      {label}
      {show_label}
      {height}
      {representations}
      {config}
      {confidenceLabel}
      {moldata}
      {errors}
      i18n={gradio.i18n}
      molviewer={showviewer}
    />
  {:else}
    <FileUpload
      {label}
      {show_label}
      {value}
      {file_count}
      {file_types}
      selectable={_selectable}
      {root}
      {height}
      {representations}
      {config}
      {confidenceLabel}
      {moldata}
      molviewer={showviewer}
      on:change={({ detail }) => {
        errors = [];
        value = detail;
      }}
      on:drag={({ detail }) => (dragging = detail)}
      on:clear={() => gradio.dispatch("clear")}
      on:select={({ detail }) => gradio.dispatch("select", detail)}
      on:notfound={() =>
        gradio.dispatch(
          "error",
          "identifier not found in database, check spelling"
        )}
      on:upload={() => gradio.dispatch("upload")}
      i18n={gradio.i18n}
    >
      <UploadText i18n={gradio.i18n} type="file" />
    </FileUpload>
  {/if}

  {#if errors.length > 0 && value !== null}
    <div
      class="flex m-2 p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400"
      role="alert"
    >
      <svg
        class="flex-shrink-0 inline w-4 h-4 mr-3 mt-[2px]"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
        />
      </svg>

      <span class="sr-only">Error in the representations</span>
      <div>
        <span class="font-medium"
          >Couldn't display Molecule. Fix the following problems:</span
        >
        <ul class="mt-1.5 ml-4 list-disc list-inside">
          {#each errors as error}
            <li>{error}</li>
          {/each}
        </ul>
      </div>
    </div>
  {/if}
</Block>

<style>
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
  .mb-4 {
    margin-bottom: 1rem;
  }
  .ml-4 {
    margin-left: 1rem;
  }
  .mr-3 {
    margin-right: 0.75rem;
  }
  .mt-1 {
    margin-top: 0.25rem;
  }
  .mt-1\.5 {
    margin-top: 0.375rem;
  }
  .mt-\[2px\] {
    margin-top: 2px;
  }
  .inline {
    display: inline;
  }
  .flex {
    display: flex;
  }
  .h-4 {
    height: 1rem;
  }
  .w-4 {
    width: 1rem;
  }
  .flex-shrink-0 {
    flex-shrink: 0;
  }
  .list-inside {
    list-style-position: inside;
  }
  .list-disc {
    list-style-type: disc;
  }
  .rounded-lg {
    border-radius: 0.5rem;
  }
  .bg-red-50 {
    --tw-bg-opacity: 1;
    background-color: rgb(254 242 242 / var(--tw-bg-opacity));
  }
  .m-2 {
    margin: 0.5rem;
  }
  .p-4 {
    padding: 1rem;
  }
  .text-sm {
    font-size: 0.875rem;
    line-height: 1.25rem;
  }
  .font-medium {
    font-weight: 500;
  }
  .lowercase {
    text-transform: lowercase;
  }
  .text-red-800 {
    --tw-text-opacity: 1;
    color: rgb(153 27 27 / var(--tw-text-opacity));
  }
  @media (prefers-color-scheme: dark) {
    .dark\:bg-gray-800 {
      --tw-bg-opacity: 1;
      background-color: rgb(31 41 55 / var(--tw-bg-opacity));
    }
    .dark\:text-red-400 {
      --tw-text-opacity: 1;
      color: rgb(248 113 113 / var(--tw-text-opacity));
    }
  }
</style>
