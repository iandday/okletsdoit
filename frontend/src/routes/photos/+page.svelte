<script lang="ts">
    import { enhance } from "$app/forms";
    import { invalidateAll } from "$app/navigation";
    import ComingSoon from "$lib/components/ComingSoon.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import "photoswipe/dist/photoswipe.css";
    import { onMount } from "svelte";
    import type { IComingSoon } from "../../types";
    import type { PageData, ActionData } from "./$types";

    const comingSoon: IComingSoon = {
        icon: "camera",
        alert: "Coming Soon",
        intro: "We're building a special place where you can upload and share your favorite photos from our big day! This feature will be available starting on our wedding day.",
        expectations: [
            { text: "Easy photo uploads", icon: "upload" },
            { text: "Browse photos from all our guests", icon: "eye" },
            { text: "Download and share your favorites", icon: "download" },
            { text: "Create lasting memories together", icon: "heart" },
        ],
    };

    let { data, form }: { data: PageData; form: ActionData } = $props();

    let uploadForm: HTMLFormElement | undefined;
    let photoInput: HTMLInputElement | undefined;
    let selectedPhotoName = "";
    let socket: WebSocket | undefined;
    let reconnectTimer: ReturnType<typeof setTimeout> | undefined;
    let reconnectAttempts = 0;
    let shouldReconnect = true;

    const connectPhotoUpdates = () => {
        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const wsUrl = `${protocol}://${window.location.host}/ws/photos/`;

        socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            reconnectAttempts = 0;
        };

        socket.onmessage = async (event: MessageEvent<string>) => {
            try {
                const payload = JSON.parse(event.data) as { event?: string };
                if (payload.event === "photo.ready" || payload.event === "photo.failed") {
                    await invalidateAll();
                }
            } catch {
                // Ignore malformed websocket payloads.
            }
        };

        socket.onclose = () => {
            if (!shouldReconnect) return;
            reconnectAttempts += 1;
            const delay = Math.min(10000, 1000 * reconnectAttempts);
            reconnectTimer = setTimeout(connectPhotoUpdates, delay);
        };

        socket.onerror = () => {
            socket?.close();
        };
    };

    onMount(() => {
        let lightbox: any;

        const setupLightbox = async () => {
            const { default: PhotoSwipeLightbox } = await import("photoswipe/lightbox");
            lightbox = new PhotoSwipeLightbox({
                gallery: "#photoswipe-gallery",
                children: "a",
                pswpModule: () => import("photoswipe"),
                bgOpacity: 0.9,
            });

            lightbox.on("uiRegister", () => {
                if (!lightbox) return;

                lightbox.pswp.ui.registerElement({
                    name: "download-button",
                    order: 8,
                    isButton: true,
                    className: "pswp__button pswp__button--download",
                    title: "Download image",
                    html: {
                        isCustomSVG: true,
                        inner: '<path d="M9.5 4.5h5v7.8l2.4-2.4 1.4 1.4-4.8 4.8-4.8-4.8 1.4-1.4 2.4 2.4z"/><path d="M5 18.5h14v2H5z"/>',
                        outlineID: "pswp__icn-download",
                        size: 24,
                    },
                    onClick: (_event: MouseEvent, _el: HTMLElement, pswp: any) => {
                        const photoId = pswp.currSlide?.data?.element?.dataset?.photoId as string | undefined;
                        if (!photoId) return;

                        window.location.assign(`/api/photos/uploaded/${photoId}/download`);
                    },
                });

                lightbox.pswp.ui.registerElement({
                    name: "counter-indicator",
                    order: 9,
                    isButton: false,
                    appendTo: "bar",
                    className: "pswp__custom-counter",
                    html: "1 / 1",
                    onInit: (el: HTMLElement, pswp: any) => {
                        const updateCounter = () => {
                            el.textContent = `${pswp.currIndex + 1} / ${pswp.getNumItems()}`;
                        };

                        pswp.on("change", updateCounter);
                        pswp.on("afterInit", updateCounter);
                    },
                });
            });

            lightbox.init();
        };

        setupLightbox();
        connectPhotoUpdates();

        return () => {
            shouldReconnect = false;
            if (reconnectTimer) {
                clearTimeout(reconnectTimer);
            }
            socket?.close();
            lightbox?.destroy();
        };
    });

    function handlePhotoChange() {
        if (!photoInput?.files?.length) return;

        selectedPhotoName = photoInput.files[0].name;
        uploadForm?.requestSubmit();
    }
</script>

<div>
    <PageShell title="Share Your Photos">
        {#if !data?.configData?.allowPhotos}
            <ComingSoon {...comingSoon} />
        {:else}
            <div>
                <p class="mt-2 text-base-content text-center">
                    Browse and share your favorite photos from our big day!
                </p>
                <p class="mt-1 text-center text-sm text-base-content pb-4">
                    Tap a photo to open it. Use swipe or arrows to navigate.
                </p>

                {#if form?.error}
                    <div class="alert alert-error">
                        <span class="icon-[lucide--alert-circle] size-5"></span>
                        <span>{form.error}</span>
                    </div>
                {/if}

                <form
                    bind:this={uploadForm}
                    method="POST"
                    action="?/uploadImage"
                    enctype="multipart/form-data"
                    use:enhance={() => {
                        return async ({ result, update }) => {
                            if (result.type === "success") {
                                selectedPhotoName = "";
                                if (photoInput) {
                                    photoInput.value = "";
                                }
                                await update({ invalidateAll: true });
                                return;
                            }

                            await update();
                        };
                    }}>
                    <input
                        id="photo-file"
                        bind:this={photoInput}
                        name="image"
                        type="file"
                        accept="image/*"
                        class="hidden"
                        onchange={handlePhotoChange} />

                    <div class="flex flex-col items-center gap-4">
                        <label for="photo-file" class="btn btn-accent btn-lg w-full sm:w-auto">
                            <span class="icon-[lucide--camera] size-5"></span>
                            Add to the gallery
                        </label>

                        {#if selectedPhotoName}
                            <div class="badge badge-outline badge-lg">
                                Selected: {selectedPhotoName}
                            </div>
                        {/if}
                    </div>
                </form>
                <div class="space-y-3 py-4">
                    <div id="photo-gallery" class="mx-auto max-w-6xl bg-base-300 py-2 px-2 shadow-md">
                        {#if data.photos.length === 0}
                            <div class="mt-6 text-center text-primary-content">
                                No photos yet, yours can be the first!
                            </div>
                        {:else}
                            <div id="photoswipe-gallery" class="mt-6 columns-3 gap-3 px-2 md:columns-4 lg:columns-5">
                                {#each data.photos as photo (photo.id)}
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
                </div>
            </div>
        {/if}
    </PageShell>
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
