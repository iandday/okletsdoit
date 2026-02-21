<script lang="ts">
    import { SvelteURLSearchParams } from "svelte/reactivity";

    type ExportResourceType = "guest" | "guest_group";

    type iExportDataProps = {
        resourceType: ExportResourceType;
        label: string;
        format: "csv" | "xlsx";
        fileName?: string;
        size?: "sm" | "md" | "lg";
    };

    const { resourceType, label, format, fileName, size = "md" }: iExportDataProps = $props();

    const sizeClasses = {
        sm: "btn-sm gap-1",
        md: "btn-md gap-2",
        lg: "btn-lg gap-3",
    };

    const iconSizes = {
        sm: "size-4",
        md: "size-6",
        lg: "size-7",
    };

    let isExporting = $state(false);
    const exportData = async () => {
        isExporting = true;
        try {
            const params = new SvelteURLSearchParams({
                resource: resourceType,
                format: format,
            });

            if (fileName) {
                params.append("fileName", fileName);
            }

            const response = await fetch(`/export?${params}`, {
                method: "GET",
                credentials: "include",
            });

            if (!response.ok) {
                throw new Error(`Export failed: ${response.statusText}`);
            }

            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = downloadUrl;

            // Extract filename from Content-Disposition or use provided fileName
            const contentDisposition = response.headers.get("Content-Disposition");
            const fileNameMatch = contentDisposition?.match(/filename="(.+)"/);
            link.download = fileNameMatch?.[1] || fileName || `export.${format}`;

            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);
        } catch (error) {
            console.error("Export error:", error);
            alert("Failed to export data. Please try again.");
        } finally {
            isExporting = false;
        }
    };
</script>

<button class="btn btn-secondary {sizeClasses[size]}" disabled={isExporting} onclick={exportData}>
    <span class="icon-[lucide--download] {iconSizes[size]}"></span>
    {isExporting ? "Exporting..." : label}
</button>
