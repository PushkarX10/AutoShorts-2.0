/**
 * AutoShorts 2.0 — Web Studio Logic & SSE Controller
 */

let selectedVideoFilename = null;
let selectedHumorStyle = "wholesome";
let activeJobId = null;
let eventSource = null;

document.addEventListener("DOMContentLoaded", () => {
  initStatus();
  initInputs();
  initUpload();
  initStyleSelector();
  initLibrary();

  document.getElementById("btn-sample-video").addEventListener("click", handleGenerateSample);
  document.getElementById("btn-generate").addEventListener("click", handleStartGeneration);
});

// ── Toast Notification ─────────────────────────────────────────────────────

function showToast(message, icon = "✓") {
  const toast = document.getElementById("toast-notification");
  const msgEl = document.getElementById("toast-message");
  const iconEl = document.getElementById("toast-icon");
  if (!toast || !msgEl) return;

  msgEl.textContent = message;
  iconEl.textContent = icon;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 2800);
}

// ── Copy to Clipboard Helper ───────────────────────────────────────────────

function copyToClipboard(elementId, label) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = el.innerText || el.textContent;
  navigator.clipboard.writeText(text).then(() => {
    showToast(`Copied ${label} to clipboard!`);
  });
}

// ── System Status ──────────────────────────────────────────────────────────

async function initStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();

    const ollamaDot = document.getElementById("status-ollama-dot");
    const ollamaText = document.getElementById("status-ollama-text");
    if (data.ollama && data.ollama.online) {
      ollamaDot.classList.add("active");
      ollamaText.textContent = `Ollama (${data.ollama.model})`;
    } else {
      ollamaDot.classList.remove("active");
      ollamaText.textContent = "Ollama Offline";
    }

    const ffmpegDot = document.getElementById("status-ffmpeg-dot");
    const ffmpegText = document.getElementById("status-ffmpeg-text");
    if (data.ffmpeg) {
      ffmpegDot.classList.add("active");
      ffmpegText.textContent = "FFmpeg Ready";
    } else {
      ffmpegDot.classList.remove("active");
      ffmpegText.textContent = "FFmpeg Missing";
    }
  } catch (e) {
    console.error("Status check failed:", e);
  }
}

// ── Input Video List ───────────────────────────────────────────────────────

async function initInputs() {
  const listEl = document.getElementById("video-list");
  listEl.innerHTML = '<div style="color:var(--text-muted);font-size:12px;">Loading clips…</div>';

  try {
    const res = await fetch("/api/inputs");
    const data = await res.json();
    listEl.innerHTML = "";

    if (!data.videos || data.videos.length === 0) {
      listEl.innerHTML = '<div style="color:var(--text-muted);font-size:12px;padding:8px;">No video clips found in input/ directory. Upload one or generate a sample!</div>';
      return;
    }

    data.videos.forEach((v, idx) => {
      const item = document.createElement("div");
      item.className = "video-item" + (idx === 0 ? " selected" : "");
      if (idx === 0) selectedVideoFilename = v.filename;

      item.innerHTML = `
        <div class="video-item-info">
          <span class="video-item-name" title="${v.filename}">${v.filename}</span>
          <span class="video-item-meta">${v.resolution} • ${v.duration ? v.duration.toFixed(1) + 's' : ''} • ${v.size_mb} MB</span>
        </div>
        <span style="color:var(--accent-cyan);font-size:14px;">▶</span>
      `;

      item.addEventListener("click", () => {
        document.querySelectorAll(".video-item").forEach(el => el.classList.remove("selected"));
        item.classList.add("selected");
        selectedVideoFilename = v.filename;
      });

      listEl.appendChild(item);
    });
  } catch (e) {
    listEl.innerHTML = '<div style="color:var(--accent-pink);font-size:12px;">Failed to load videos</div>';
  }
}

// ── File Upload (Dropzone) ─────────────────────────────────────────────────

function initUpload() {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");

  dropzone.addEventListener("click", () => fileInput.click());

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("drag-over");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("drag-over");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("drag-over");
    if (e.dataTransfer.files.length > 0) {
      uploadFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      uploadFile(e.target.files[0]);
    }
  });
}

async function uploadFile(file) {
  showToast(`Uploading ${file.name}…`, "⏳");
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    if (res.ok) {
      showToast(`Uploaded ${data.filename}!`);
      selectedVideoFilename = data.filename;
      await initInputs();
    } else {
      showToast("Upload failed", "❌");
    }
  } catch (e) {
    showToast("Upload error", "❌");
  }
}

async function handleGenerateSample() {
  const btn = document.getElementById("btn-sample-video");
  btn.disabled = true;
  btn.innerHTML = `<span>⏳</span> Generating Neon Parkour Demo…`;
  showToast("Rendering 35s demo parkour clip…", "🎮");

  try {
    const res = await fetch("/api/sample-video", { method: "POST" });
    const data = await res.json();
    if (res.ok) {
      showToast("Demo clip created!", "✓");
      selectedVideoFilename = data.filename;
      await initInputs();
    }
  } catch (e) {
    showToast("Sample generation error", "❌");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>🎮</span> Generate Sample Parkour Clip`;
  }
}

// ── Style Selector ─────────────────────────────────────────────────────────

function initStyleSelector() {
  const cards = document.querySelectorAll(".style-card");
  cards.forEach(c => {
    c.addEventListener("click", () => {
      cards.forEach(x => x.classList.remove("selected"));
      c.classList.add("selected");
      selectedHumorStyle = c.getAttribute("data-style");
    });
  });
}

// ── Start Generation ───────────────────────────────────────────────────────

async function handleStartGeneration() {
  if (!selectedVideoFilename) {
    showToast("Please select or upload a video clip first!", "⚠️");
    return;
  }

  const customTheme = document.getElementById("input-custom-theme").value.trim();
  const btnGen = document.getElementById("btn-generate");
  btnGen.disabled = true;
  btnGen.innerHTML = `<span>⏳</span> Processing AutoShort…`;

  // Reset UI
  document.getElementById("progress-fill").style.width = "0%";
  document.getElementById("progress-pct").textContent = "0%";
  document.getElementById("progress-stage-name").textContent = "Initializing…";
  document.querySelectorAll(".stage-pill").forEach(p => p.classList.remove("active", "completed"));
  const term = document.getElementById("terminal-logs");
  term.innerHTML = "";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        video_filename: selectedVideoFilename,
        humor_style: selectedHumorStyle,
        theme: customTheme || null,
        character_count: 2,
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      showToast(data.detail || "Failed to start generation", "❌");
      btnGen.disabled = false;
      btnGen.innerHTML = `<span>🚀</span> Generate YouTube Short`;
      return;
    }

    activeJobId = data.job_id;
    startSSEStream(activeJobId);
  } catch (e) {
    showToast("Connection error", "❌");
    btnGen.disabled = false;
    btnGen.innerHTML = `<span>🚀</span> Generate YouTube Short`;
  }
}

// ── Server-Sent Events (SSE) Stream ────────────────────────────────────────

const STAGES = [
  "inspecting",
  "generating_conversation",
  "generating_voices",
  "building_timeline",
  "compositing",
  "encoding",
  "validating",
  "generating_metadata",
  "completed",
];

function startSSEStream(jobId) {
  if (eventSource) eventSource.close();

  eventSource = new EventSource(`/api/jobs/${jobId}/stream`);

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.progress_pct !== undefined) {
      document.getElementById("progress-fill").style.width = `${data.progress_pct}%`;
      document.getElementById("progress-pct").textContent = `${data.progress_pct}%`;
    }

    if (data.status) {
      document.getElementById("progress-stage-name").textContent = formatStatusName(data.status);
      updateStagePills(data.status);
    }

    if (data.new_logs && data.new_logs.length > 0) {
      appendLogs(data.new_logs);
    }

    if (data.status === "completed") {
      eventSource.close();
      handleJobCompleted(jobId, data);
    } else if (data.status === "failed") {
      eventSource.close();
      handleJobFailed(data.error);
    }
  };

  eventSource.onerror = () => {
    eventSource.close();
  };
}

function formatStatusName(status) {
  return status.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}

function updateStagePills(currentStatus) {
  const curIdx = STAGES.indexOf(currentStatus);
  STAGES.forEach((s, idx) => {
    const pill = document.getElementById(`stage-${s}`);
    if (!pill) return;
    if (idx < curIdx) {
      pill.classList.remove("active");
      pill.classList.add("completed");
    } else if (idx === curIdx) {
      pill.classList.add("active");
      pill.classList.remove("completed");
    } else {
      pill.classList.remove("active", "completed");
    }
  });
}

function appendLogs(logs) {
  const term = document.getElementById("terminal-logs");
  logs.forEach(l => {
    const div = document.createElement("div");
    div.className = "log-line";
    const lvlClass = l.level === "SUCCESS" ? "log-success" : l.level === "ERROR" ? "log-error" : "log-info";
    div.innerHTML = `
      <span class="log-time">[${l.timestamp}]</span>
      <span class="${lvlClass}">${l.message}</span>
    `;
    term.appendChild(div);
  });
  term.scrollTop = term.scrollHeight;
}

// ── Job Completion Handling ────────────────────────────────────────────────

async function handleJobCompleted(jobId, data) {
  const btnGen = document.getElementById("btn-generate");
  btnGen.disabled = false;
  btnGen.innerHTML = `<span>🚀</span> Generate Another Short`;

  showToast("Short Rendered Successfully!", "🎉");

  // Fetch full details
  const res = await fetch(`/api/jobs/${jobId}`);
  const details = await res.json();
  const job = details.job;

  // Video Preview
  const videoEl = document.getElementById("preview-video");
  const placeholder = document.getElementById("preview-placeholder");
  if (details.video_url) {
    videoEl.src = details.video_url;
    videoEl.style.display = "block";
    placeholder.style.display = "none";
    videoEl.play();
  }

  // YouTube SEO
  if (job.youtube_metadata) {
    document.getElementById("seo-card").style.display = "flex";
    document.getElementById("seo-title").textContent = job.youtube_metadata.title;
    document.getElementById("seo-desc").textContent = job.youtube_metadata.description;
    document.getElementById("seo-hashtags").textContent = (job.youtube_metadata.hashtags || []).join(" ");
    document.getElementById("seo-pinned").textContent = job.youtube_metadata.pinned_comment || "";
  }

  // Refresh Library
  initLibrary();
}

function handleJobFailed(err) {
  const btnGen = document.getElementById("btn-generate");
  btnGen.disabled = false;
  btnGen.innerHTML = `<span>🚀</span> Try Again`;
  showToast(`Generation Failed: ${err}`, "❌");
}

// ── Library / History ──────────────────────────────────────────────────────

async function initLibrary() {
  const grid = document.getElementById("library-grid");
  if (!grid) return;

  try {
    const res = await fetch("/api/library");
    const data = await res.json();
    grid.innerHTML = "";

    if (!data.library || data.library.length === 0) {
      grid.innerHTML = '<div style="color:var(--text-muted);font-size:13px;grid-column:1/-1;">No generated shorts yet. Create your first short above!</div>';
      return;
    }

    data.library.forEach(item => {
      const card = document.createElement("div");
      card.className = "library-card";
      card.innerHTML = `
        <div class="library-thumb-wrapper">
          <img class="library-thumb-img" src="${item.thumbnail_url || ''}" alt="${item.title}" onerror="this.style.display='none'">
        </div>
        <div class="library-meta">
          <div class="library-title" title="${item.title}">${item.title}</div>
          <div class="library-info-row">
            <span>⏱ ${item.duration.toFixed(1)}s • ${item.size_mb}MB</span>
            <span>📅 ${item.created_at}</span>
          </div>
          <div style="display:flex;gap:6px;margin-top:8px;">
            <a href="${item.video_url}" target="_blank" class="btn-secondary" style="padding:6px 10px;font-size:11px;text-decoration:none;">Watch</a>
            <a href="/api/download/${item.bundle_id}/zip" class="btn-secondary" style="padding:6px 10px;font-size:11px;text-decoration:none;">Download Zip</a>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
  } catch (e) {
    grid.innerHTML = '<div style="color:var(--accent-pink);font-size:13px;">Error loading library</div>';
  }
}
