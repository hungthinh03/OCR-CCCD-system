const MOCK = {
  cccd: [
    { key: "id", label: "Số CCCD", value: "", validator: v => /^\d{12}$/.test(v) },
    { key: "name", label: "Họ và tên", value: "" },
    { key: "dob", label: "Ngày sinh", value: "", validator: v => /^\d{2}\/\d{2}\/\d{4}$/.test(v) },
    { key: "sex", label: "Giới tính", value: "" },
    { key: "nationality", label: "Quốc tịch", value: "" },
    { key: "origin", label: "Quê quán", value: "" },
    { key: "address", label: "Nơi thường trú", value: "" },
    { key: "expiry", label: "Có giá trị đến", value: "", validator: v => /^\d{2}\/\d{2}\/\d{4}$/.test(v) },
  ],
  passport: [
    { key: "passportNo", label: "Số hộ chiếu", value: "", validator: v => /^[A-Z]\d{7,8}$/.test(v) },
    { key: "name", label: "Họ và tên", value: "" },
    { key: "dob", label: "Ngày sinh", value: "", validator: v => /^\d{2}\/\d{2}\/\d{4}$/.test(v) },
    { key: "sex", label: "Giới tính", value: "" },
    { key: "nationality", label: "Quốc tịch", value: "" },
    { key: "issueDate", label: "Ngày cấp", value: "", validator: v => /^\d{2}\/\d{2}\/\d{4}$/.test(v) },
    { key: "expiry", label: "Ngày hết hạn", value: "", validator: v => /^\d{2}\/\d{2}\/\d{4}$/.test(v) },
    { key: "issuingAuthority", label: "Nơi cấp", value: "" },
  ]
};

let state = { file: null, fields: [] };

const $ = id => document.getElementById(id);
const drop = $("drop"), input = $("fileInput");
const viewTabs = document.querySelectorAll("#viewTabs .sub-tab");
const emptyState = $("emptyState");
const loadingState = $("loadingState");
const resultState = $("resultState");
const elapsed = $("elapsed");
const runBtn = $("runBtn");

function setHidden(el, hidden) {
  el.classList.toggle("is-hidden", hidden);
}

function setUploadState(hasFile) {
  setHidden($("dropEmpty"), hasFile);
  setHidden($("dropPreview"), !hasFile);
  runBtn.disabled = !hasFile;
  $("resetBtn").disabled = !hasFile;
}

function showEmpty() {
  setHidden(emptyState, false);
  setHidden(loadingState, true);
  setHidden(resultState, true);
  setHidden(elapsed, true);
}

function showLoading() {
  setHidden(emptyState, true);
  setHidden(loadingState, false);
  setHidden(resultState, true);
  setHidden(elapsed, true);
}

function showResult(timeMs) {
  setHidden(emptyState, true);
  setHidden(loadingState, true);
  setHidden(resultState, false);
  setHidden(elapsed, false);
  elapsed.textContent = `⏱ ${timeMs}ms`;
}

function setView(view) {
  setHidden($("fieldsView"), view !== "fields");
  setHidden($("jsonView"), view !== "json");
  viewTabs.forEach(tab => tab.classList.toggle("active", tab.dataset.view === view));
}

function toast(msg, type = "") {
  const t = $("toast");
  t.textContent = msg;
  t.className = "toast show " + type;
  clearTimeout(window._tt);
  window._tt = setTimeout(() => t.className = "toast", 2200);
}

function renderFields(data) {
  const fields = Object.keys(data).map(key => {
    // data[key] bây giờ là một object: { value: "...", is_valid: true/false }
    const fieldData = data[key];
    const val = fieldData.value || "";
    const isValid = fieldData.is_valid;
    
    return `
      <div class="field" style="display:flex; flex-direction:column; justify-content:flex-start; text-align:left; margin-bottom: 12px;">
        <label class="lbl" style="font-weight: bold; color: #555;">${key}</label>
        <div class="val" style="display:flex; justify-content:space-between; width:100%; align-items:center; font-size:15px; padding: 4px 0; border-bottom: 1px solid #eee;">
          <span style="color: ${val ? '#333' : '#aaa'}">
            ${val ? val : '<em style="font-weight:normal;">Trống</em>'}
          </span>
          <span class="status ${isValid ? 'ok' : 'err'}" 
                style="font-size:16px; color: ${isValid ? '#28a745' : '#dc3545'};"
                title="${isValid ? 'Dữ liệu hợp lệ' : 'Dữ liệu có thể sai định dạng'}">
            ${isValid ? '✓' : '⚠'}
          </span>
        </div>
      </div>
    `;
  }).join('');
  
  $("fieldsView").innerHTML = fields;
  $("jsonOut").textContent = JSON.stringify(data, null, 2);
}

viewTabs.forEach(tab => {
  tab.onclick = () => setView(tab.dataset.view);
});

drop.onclick = () => input.click();
drop.ondragover = e => { e.preventDefault(); drop.classList.add("drag"); };
drop.ondragleave = () => drop.classList.remove("drag");
drop.ondrop = e => {
  e.preventDefault(); drop.classList.remove("drag");
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
};
input.onchange = e => e.target.files[0] && handleFile(e.target.files[0]);

function handleFile(f) {
  if (!f.type.startsWith("image/")) return toast("Vui lòng chọn tệp ảnh.", "error");
  state.file = f;
  $("previewImg").src = URL.createObjectURL(f);
  $("fileName").textContent = f.name;
  setUploadState(true);
  showEmpty();
}

$("resetBtn").onclick = () => {
  state.file = null; state.fields = [];
  input.value = "";
  setUploadState(false);
  showEmpty();
};

$("copyBtn").onclick = () => {
  navigator.clipboard.writeText($("jsonOut").textContent)
    .then(() => toast("Đã copy JSON", "success"))
    .catch(() => toast("Lỗi khi copy", "error"));
};

runBtn.onclick = async () => {
  if (!state.file) return;

  showLoading();
  const startTime = Date.now();
  const formData = new FormData();
  formData.append("file", state.file);

  try {
    const res = await fetch("/ocr", {
      method: "POST",
      body: formData
    });
    
    if (!res.ok) throw new Error("Network response was not ok");
    
    const data = await res.json();
    const timeMs = Date.now() - startTime;
    
    renderFields(data);
    showResult(timeMs);
    toast("Trích xuất thành công", "success");
    
  } catch (error) {
    console.error(error);
    showEmpty();
    toast("Có lỗi xảy ra khi trích xuất", "error");
  }
};

showEmpty();
setUploadState(false);
setView("fields");
