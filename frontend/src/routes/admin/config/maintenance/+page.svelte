<script lang="ts">
    import { enhance } from "$app/forms";

    let isRegeneratingAll = $state(false);
</script>

<div class="config-card">
    <div class="config-card-body">
        <h2 class="config-card-title text-xl mb-4">Maintenance</h2>
        <p>Run administrative maintenance tasks for guest list QR code assets.</p>

        <div class="grid grid-cols-1 gap-4 mt-4">
            <form
                method="POST"
                action="?/regenerateAllQrCodes"
                use:enhance={() => {
                    isRegeneratingAll = true;
                    return async ({ update }) => {
                        await update();
                        isRegeneratingAll = false;
                    };
                }}>
                <button type="submit" class="btn btn-warning gap-2 w-full" disabled={isRegeneratingAll}>
                    <span class="icon-[lucide--refresh-cw] size-5"></span>
                    {isRegeneratingAll ? "Regenerating..." : "Regenerate QR Codes"}
                </button>
            </form>
        </div>
    </div>
</div>
