<script lang="ts">
    import type { UploadedPhotoSchema } from "../../../api-client/models/UploadedPhotoSchema";

    type IPhotoGallery = {
        photos?: UploadedPhotoSchema[];
    };

    const { photos }: IPhotoGallery = $props();
</script>

<div id="photo-gallery" class="mx-auto max-w-6xl bg-base-300 py-2 px-2 shadow-md">
    {#if !photos || photos.length === 0}
        <div class="mt-6 text-center text-primary-content">No photos yet, yours can be the first!</div>
    {:else}
        <div id="photoswipe-gallery" class="mt-6 columns-3 gap-3 px-2 md:columns-4 lg:columns-5">
            {#each photos as photo (photo.id)}
                <div class="mb-3 break-inside-avoid">
                    <a
                        href={photo.photoFile}
                        data-photo-id={photo.id}
                        data-pswp-width={photo.width ?? 1600}
                        data-pswp-height={photo.height ?? 1200}
                        class="group relative block cursor-zoom-in overflow-hidden rounded-xl shadow-md"
                        aria-label="Open photo">
                        <img
                            src={photo.thumbnailFile}
                            alt={photo.id}
                            class="h-auto w-full rounded-xl object-cover transition-transform duration-200 group-hover:scale-[1.02]"
                            loading="lazy" />
                    </a>
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
