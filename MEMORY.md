# MEMORY.md - Long-Term Memory

## OpenClaw deployment identity

- Current OpenClaw deployment runs on Tencent Cloud.
- Default remote host: root@100.106.74.27
- Environment label: cloud-tencent
- Host label: vm-0-8-opencloudos
- For OpenClaw operations involving skills, workspace structure, deployment, routing, and troubleshooting, default to this Tencent Cloud instance unless the user explicitly switches target.
- This deployment is the cloud-side OpenClaw environment, distinct from the local Obsidian knowledge base.

## Tailscale environment mapping

- Tailscale is installed in both the local environment and the Tencent Cloud OpenClaw environment.
- Prefer Tailscale for private node-to-node access, internal SSH, and environment troubleshooting when the target node is inside the user's tailnet.
- Current known nodes:
  - cloud-tencent -> 100.106.74.27 -> host label vm-0-8-opencloudos -> current cloud OpenClaw node
  - local-cangku -> 100.106.60.94 -> Windows node -> local machine, currently seen as offline in the latest status check
  - zhang -> 100.80.231.73 -> Windows node
- Unless the user says otherwise, OpenClaw deployment work defaults to cloud-tencent.
- When the user asks about local and cloud communication, first consider whether Tailscale is the intended path.
