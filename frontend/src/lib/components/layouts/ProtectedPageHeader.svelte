<script lang="ts">
    type IProtectedPageHeader = {
        title: string;
        description?: string;
        previewLink?: string;
        previewText?: string;
        editLink?: string;
        editText?: string;
        deleteLink?: string;
        deleteText?: string;
        cancelLink?: string;
        cancelText?: string;
        showButtons?: boolean;

        children?: import("svelte").Snippet;
    };
    const {
        title,
        description = "",
        editLink = "",
        editText = "",
        deleteLink = "",
        deleteText = "",
        cancelLink = "",
        cancelText = "",
        showButtons = true,
        children,
    }: IProtectedPageHeader = $props();
</script>

<div class="w-full mb-8">
    <div class="flex justify-between items-center mb-6">
        <div class="flex flex-col">
            <h1 class="text-3xl font-bold">{title}</h1>
            {#if description}
                <span class="text-lg">{description}</span>
            {/if}
        </div>
        {#if showButtons}
            <div class="flex gap-2">
                {#if cancelLink && cancelText}
                    <a href={cancelLink} class="btn btn-error">{cancelText}</a>
                {/if}
                {#if editLink && editText}
                    <a href={editLink} class="btn btn-primary">{editText}</a>
                {/if}
                {#if deleteLink && deleteText}
                    <a href={deleteLink} class="btn btn-danger">{deleteText}</a>
                {/if}
            </div>
        {/if}
    </div>
    {@render children?.()}
</div>
