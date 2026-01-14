<script lang="ts" generics="T">
    import type { Snippet } from "svelte";
    import type { IBreadcrumb } from "../../types";
    import ProtectedPageShell from "../layouts/ProtectedPageShell.svelte";
    import ObjectStatus from "./ObjectStatus.svelte";

    type IObjectDetail<T> = {
        relativeCrumbs?: IBreadcrumb[];
        title?: string;
        status?: boolean | null;
        statusText?: string | null;
        editLink: string;
        deleteAction?: string;
        deleteRedirect?: string;
        childCreateLink?: string;
        childCreateLabel?: string;
        mainSnippet: Snippet;
        mainActionsSnippet?: Snippet;
        extraCardsSnippet?: Snippet;
        object: T;
    };

    const {
        relativeCrumbs = [],
        title,
        status = null,
        statusText = null,
        editLink,
        deleteAction,
        deleteRedirect,
        childCreateLink,
        childCreateLabel,
        mainSnippet,
        mainActionsSnippet,
        extraCardsSnippet,
        object,
    }: IObjectDetail<T> = $props();
</script>

<ProtectedPageShell {relativeCrumbs}>
    <div class="mb-6 flex items-center justify-between">
        <div>
            <h1 class="text-3xl font-bold text-base-content">{title}</h1>
            {#if status !== null}<ObjectStatus text={statusText} {status} />{/if}
        </div>
        <div class="flex gap-2">
            <a class="btn btn-success gap-2" href={editLink}> Edit </a>
            {#if deleteAction}
                <form
                    method="POST"
                    action={deleteAction}
                    onsubmit={(e) => {
                        if (!confirm("Are you sure you want to delete this item? This action cannot be undone.")) {
                            e.preventDefault();
                        }
                    }}>
                    {#if deleteRedirect}
                        <input type="hidden" name="redirect" value={deleteRedirect} />
                    {/if}
                    <button type="submit" class="btn btn-error gap-2"> Delete </button>
                </form>
            {/if}
        </div>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="detail-card" id="main-info">
            <div class="detail-card-body">
                <div class="detail-card-title">Item Details</div>
                {@render mainSnippet()}
            </div>
            {#if mainActionsSnippet}
                <div class="detail-card-actions flex gap-2">{@render mainActionsSnippet()}</div>
            {/if}
        </div>
        <div class="detail-card" id="metadata">
            <div class="detail-card-body">
                <div class="detail-card-title">Record Information</div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <div class="detail-card-field-name">Created By</div>
                        <div class="detail-card-field-value">{object.createdByName}</div>
                    </div>
                    <div>
                        <div class="detail-card-field-name">Created At</div>
                        <div class="detail-card-field-value">{object.createdAt}</div>
                    </div>
                    <div>
                        <div class="detail-card-field-name">Last Updated By</div>
                        <div class="detail-card-field-value">{object.updatedByName}</div>
                    </div>
                    <div>
                        <div class="detail-card-field-name">Last Updated At</div>
                        <div class="detail-card-field-value">{object.updatedAt}</div>
                    </div>
                </div>
            </div>
        </div>

        {#if extraCardsSnippet}
            {@render extraCardsSnippet()}
        {/if}
    </div>
</ProtectedPageShell>
