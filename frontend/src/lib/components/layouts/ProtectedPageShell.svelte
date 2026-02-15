<script lang="ts">
    import Topbar from "$lib/components/layouts/Topbar.svelte";
    import type { iBreadcrumb } from "$lib/types";
    import { fly } from "svelte/transition";
    import Breadcrumbs from "./Breadcrumbs.svelte";

    type iProtectedPageShellProps = {
        relativeCrumbs: iBreadcrumb[] | [];
        form?: { success?: boolean; error?: string; message?: string } | null;
        children?: import("svelte").Snippet;
    };
    const { relativeCrumbs, form, children }: iProtectedPageShellProps = $props();

    let baseCrumbs: iBreadcrumb[] = [
        { title: "Home", href: "/" },
        { title: "Planning", href: "/planning" },
    ];

    let crumbs: iBreadcrumb[] = [...baseCrumbs, ...relativeCrumbs];

    // Toast notification state
    let showToast = $state(false);
    let toastMessage = $state("");
    let toastType = $state<"success" | "error">("success");

    // Watch for form responses and trigger toast
    $effect(() => {
        if (form?.success || form?.error) {
            toastMessage = form.message || form.error || "";
            toastType = form.success ? "success" : "error";
            showToast = true;

            // Auto-dismiss after 3 seconds
            setTimeout(() => {
                showToast = false;
            }, 3000);
        }
    });
</script>

<div>
    <!-- Toast Notification -->
    {#if showToast}
        <div class="toast toast-top toast-end z-100" transition:fly={{ x: 200, duration: 300 }}>
            <div class="alert {toastType === 'success' ? 'alert-success' : 'alert-error'} shadow-lg">
                {#if toastType === "success"}
                    <span class="icon-[lucide--check-circle] size-6"></span>
                {:else}
                    <span class="icon-[lucide--alert-circle] size-6"></span>
                {/if}
                <span>{toastMessage}</span>
            </div>
        </div>
    {/if}

    <Topbar />
    <div class="pt-2 px-6 pb-8 lg:pb-16 xl:pb-24 2xl:pb-28">
        <Breadcrumbs breadcrumbs={crumbs} />
        <div class="container mx-auto p-4">
            {@render children?.()}
        </div>
    </div>
</div>
