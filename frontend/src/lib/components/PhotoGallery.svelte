<script lang="ts">
    import type { UploadedPhotoSchema } from "../../../api-client/models/UploadedPhotoSchema";

    type IPhotoGallery = {
        photos?: UploadedPhotoSchema[];
        adminMode?: boolean;
        deleteAction?: string;
        restoreAction?: string;
        approveAction?: string;
        unapproveAction?: string;
    };

    const {
        photos,
        adminMode = false,
        deleteAction = "?/deletePhoto",
        restoreAction = "?/restorePhoto",
        approveAction = "?/approvePhoto",
        unapproveAction = "?/unapprovePhoto",
    }: IPhotoGallery = $props();
</script>

<div id="photo-gallery" class="mx-auto max-w-6xl bg-base-300 py-2 px-2 shadow-md">
    {#if !photos || photos.length === 0}
        <div class="mt-6 text-center text-primary-content">No photos yet, yours can be the first!</div>
    {:else}
        <div id="photoswipe-gallery" class="mt-6 columns-3 gap-3 px-2 md:columns-4 lg:columns-5">
            {#each photos as photo (photo.id)}
                <div class="mb-3 break-inside-avoid">
                    <div class="group relative overflow-hidden rounded-xl shadow-md">
                        <a
                            href={photo.photoFile}
                            data-photo-id={photo.id}
                            data-pswp-width={photo.width ?? 1600}
                            data-pswp-height={photo.height ?? 1200}
                            class="block cursor-zoom-in"
                            aria-label="Open photo">
                            <img
                                src={photo.thumbnailFile}
                                alt={photo.id}
                                class="h-auto w-full rounded-xl object-cover transition-transform duration-200 group-hover:scale-[1.02]"
                                loading="lazy" />
                        </a>

                        {#if adminMode}
                            <div class="absolute right-2 top-2 z-10 flex flex-row gap-2">
                                <form method="POST" action={photo.isDeleted ? restoreAction : deleteAction}>
                                    <input type="hidden" name="photoId" value={photo.id} />
                                    <button
                                        type="submit"
                                        class={photo.isDeleted ? "btn btn-success btn-xs" : "btn btn-error btn-xs"}
                                        aria-label={photo.isDeleted ? "Restore photo" : "Delete photo"}
                                        onclick={(event) => {
                                            if (
                                                !confirm(
                                                    photo.isDeleted
                                                        ? "Restore this photo to the gallery?"
                                                        : "Delete this photo from the gallery?",
                                                )
                                            ) {
                                                event.preventDefault();
                                            }
                                        }}>
                                        {photo.isDeleted ? "Restore" : "Delete"}
                                    </button>
                                </form>

                                <form method="POST" action={photo.isApproved ? unapproveAction : approveAction}>
                                    <input type="hidden" name="photoId" value={photo.id} />
                                    <button
                                        type="submit"
                                        class={photo.isApproved ? "btn btn-warning btn-xs" : "btn btn-info btn-xs"}
                                        aria-label={photo.isApproved ? "Unapprove photo" : "Approve photo"}
                                        onclick={(event) => {
                                            if (
                                                !confirm(
                                                    photo.isApproved
                                                        ? "Mark this photo as unapproved?"
                                                        : "Approve this photo for guests?",
                                                )
                                            ) {
                                                event.preventDefault();
                                            }
                                        }}>
                                        {photo.isApproved ? "Unapprove" : "Approve"}
                                    </button>
                                </form>
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    :global(.pswp__button--download) {
        align-items: center;
        display: inline-flex;
        font-size: 20px;
        justify-content: center;
        text-decoration: none;
    }

    :global(.pswp__custom-counter) {
        color: #fff;
        font-size: 14px;
        font-weight: 600;
        line-height: 1;
        margin-left: 12px;
        opacity: 0.85;
        padding-top: 16px;
    }
</style>
