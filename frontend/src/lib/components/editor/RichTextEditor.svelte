<script lang="ts">
    import { Editor } from "@tiptap/core";
    import Link from "@tiptap/extension-link";
    import Placeholder from "@tiptap/extension-placeholder";
    import StarterKit from "@tiptap/starter-kit";
    import { onMount, onDestroy } from "svelte";

    let {
        value = $bindable(""),
        placeholder = "Start typing...",
        name = "content",
    }: {
        value?: string;
        placeholder?: string;
        name?: string;
    } = $props();

    let editor: Editor | null = null;
    let element: HTMLDivElement;
    let hiddenInput: HTMLTextAreaElement;

    onMount(() => {
        editor = new Editor({
            element: element,
            extensions: [
                StarterKit,
                Link.configure({
                    openOnClick: false,
                    HTMLAttributes: {
                        class: "link link-primary",
                    },
                }),
                Placeholder.configure({
                    placeholder: placeholder,
                }),
            ],
            content: value,
            onTransaction: () => {
                editor = editor;
            },
            onUpdate: ({ editor }) => {
                const html = editor.getHTML();
                value = html === "<p></p>" ? "" : html;
                if (hiddenInput) {
                    hiddenInput.value = value;
                }
            },
            editorProps: {
                attributes: {
                    class: "prose prose-sm sm:prose lg:prose-lg xl:prose-xl focus:outline-none min-h-[200px] max-w-none p-4",
                },
            },
        });
    });

    onDestroy(() => {
        if (editor) {
            editor.destroy();
        }
    });

    function toggleBold() {
        editor?.chain().focus().toggleBold().run();
    }

    function toggleItalic() {
        editor?.chain().focus().toggleItalic().run();
    }

    function toggleBulletList() {
        editor?.chain().focus().toggleBulletList().run();
    }

    function toggleOrderedList() {
        editor?.chain().focus().toggleOrderedList().run();
    }

    function setLink() {
        const url = window.prompt("Enter URL:");
        if (url) {
            editor?.chain().focus().setLink({ href: url }).run();
        }
    }

    function removeLink() {
        editor?.chain().focus().unsetLink().run();
    }

    $effect(() => {
        if (editor && value !== editor.getHTML()) {
            editor.commands.setContent(value || "");
        }
    });
</script>

<div class="border border-base-300 rounded-lg bg-base-100">
    <!-- Toolbar -->
    <div class="border-b border-base-300 p-2 flex gap-1 flex-wrap">
        <button
            type="button"
            onclick={toggleBold}
            class="btn btn-sm btn-ghost"
            class:btn-active={editor?.isActive("bold")}
            title="Bold (Ctrl+B)">
            <span class="icon-[lucide--bold] size-4"></span>
        </button>
        <button
            type="button"
            onclick={toggleItalic}
            class="btn btn-sm btn-ghost"
            class:btn-active={editor?.isActive("italic")}
            title="Italic (Ctrl+I)">
            <span class="icon-[lucide--italic] size-4"></span>
        </button>
        <div class="divider divider-horizontal mx-0"></div>
        <button
            type="button"
            onclick={toggleBulletList}
            class="btn btn-sm btn-ghost"
            class:btn-active={editor?.isActive("bulletList")}
            title="Bullet List">
            <span class="icon-[lucide--list] size-4"></span>
        </button>
        <button
            type="button"
            onclick={toggleOrderedList}
            class="btn btn-sm btn-ghost"
            class:btn-active={editor?.isActive("orderedList")}
            title="Numbered List">
            <span class="icon-[lucide--list-ordered] size-4"></span>
        </button>
        <div class="divider divider-horizontal mx-0"></div>
        <button
            type="button"
            onclick={setLink}
            class="btn btn-sm btn-ghost"
            class:btn-active={editor?.isActive("link")}
            title="Add Link">
            <span class="icon-[lucide--link] size-4"></span>
        </button>
        {#if editor?.isActive("link")}
            <button type="button" onclick={removeLink} class="btn btn-sm btn-ghost" title="Remove Link">
                <span class="icon-[lucide--link-2-off] size-4"></span>
            </button>
        {/if}
    </div>

    <!-- Editor -->
    <div bind:this={element} class="edit-card-field-input min-h-[200px]"></div>

    <!-- Hidden input for form submission -->
    <textarea bind:this={hiddenInput} {name} class="hidden" {value}></textarea>
</div>

<style>
    :global(.ProseMirror) {
        min-height: 200px;
        padding: 1rem;
    }

    :global(.ProseMirror:focus) {
        outline: none;
    }

    :global(.ProseMirror p.is-editor-empty:first-child::before) {
        content: attr(data-placeholder);
        float: left;
        color: hsl(var(--bc) / 0.4);
        pointer-events: none;
        height: 0;
    }

    :global(.ProseMirror ul),
    :global(.ProseMirror ol) {
        padding-left: 1.5rem;
        margin: 0.5rem 0;
    }

    :global(.ProseMirror ul) {
        list-style-type: disc;
    }

    :global(.ProseMirror ol) {
        list-style-type: decimal;
    }

    :global(.ProseMirror li) {
        margin: 0.25rem 0;
    }

    :global(.ProseMirror h1),
    :global(.ProseMirror h2),
    :global(.ProseMirror h3) {
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    :global(.ProseMirror h1) {
        font-size: 2rem;
    }

    :global(.ProseMirror h2) {
        font-size: 1.5rem;
    }

    :global(.ProseMirror h3) {
        font-size: 1.25rem;
    }

    :global(.ProseMirror p) {
        margin: 0.5rem 0;
    }

    :global(.ProseMirror strong) {
        font-weight: bold;
    }

    :global(.ProseMirror em) {
        font-style: italic;
    }

    :global(.ProseMirror a) {
        color: hsl(var(--p));
        text-decoration: underline;
    }

    :global(.ProseMirror a:hover) {
        opacity: 0.8;
    }
</style>
