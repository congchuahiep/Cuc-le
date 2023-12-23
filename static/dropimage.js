// Nguồn: https://www.youtube.com/watch?v=5Fws9daTtIs

const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");
const form = document.getElementById("edit-image");
const inputWatermark = document.getElementById("edit-input-watermark");
const cancelWatermark = document.getElementById("cancel-upload-watermark");
const selectFrame = document.getElementById("edit-frame");
const downloadButton = document.getElementById("downloadButton")


let debounceTimer;
inputFile.addEventListener("change", uploadImage);
inputWatermark.addEventListener("change", uploadWatermark);
selectFrame.addEventListener('change', updateSelectFrame);
form.addEventListener("input", function () {
  // Hủy bỏ bất kỳ hẹn giờ trước đó
  clearTimeout(debounceTimer);

  // Đặt hẹn giờ mới
  debounceTimer = setTimeout(function () {
    // Gọi hàm tự động gửi form sau khi người dùng đã nghỉ trạng thái nhập trong 0.5 giây
    autoSubmitForm();
  }, 500); // Thời gian debounce: 500ms (0.5 giây)
});
var nameImage = ""
var nameWatermark = ""

// Tải ảnh lên server
function uploadImage() {
  // Lấy dữ liệu file upload
  // Lưu ý rằng ban đầu file upload lên có chứa dấu '(' và ')'
  // Và vì một số lí do nên chúng ta phải sử lí dấu '(' và ')'
  // Để có thể chạy ổn định
  const file_old = inputFile.files[0];

  // Xử lí dấu '(' và ')'
  const currentFileName = file_old.name;
  const newFileName = currentFileName.replace(/[()]/g, '');


  // Tạo file mới, có tên được xử lí dấu '(' và ')'
  const file = new File([file_old], newFileName, { type: file_old.type });

  console.log(file.name);
  nameImage = file.name;
  const formData = new FormData();
  formData.append('file', file);

  // Tôi thực sự chả hiểu mấy dòng này
  // Nôm na là gửi file lên server bằng fetch API
  if (file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(data => {
        // Check thông tin
        console.log(data);

        // Thay đổi ô chứa ảnh thành tấm ảnh
        let imgLink = URL.createObjectURL(file);
        imageView.style.backgroundImage = `url(${imgLink})`;
        imageView.textContent = "";
        imageView.style.border = 0;
        imageView.classList.add("dim");

        // Upload thành công sẽ mở form
        var openForm = document.querySelectorAll('[id^="edit-"]');
        openForm.forEach(function (openForm) {
          openForm.disabled = false;
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
}

const textWatermark = document.getElementById("edit-text-watermark");
const selectedLayoutWatermark = document.getElementById("setWatermarkLayout");
// Tải watermark lên server
function uploadWatermark() {
  const file = inputWatermark.files[0];
  nameWatermark = inputWatermark.files[0].name;
  const formData = new FormData();
  formData.append('file', file);

  if (file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_watermark', {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(data => {
        // Check thông tin
        console.log(data);

        // Upload thành công sẽ mở form watermark, đóng form text, mở nút cancel
        selectedLayoutWatermark.disabled = false;
        cancelWatermark.disabled = false;
        textWatermark.disabled = true;

      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
}

function clearFileInput() {

  cancelWatermark.disabled = true;
  // Đặt giá trị của file input thành null để làm trống
  inputWatermark.value = null;
  textWatermark.disabled = false;
  selectedLayoutWatermark.disabled = true;
  fetch('/cancel_watermark', {
    method: 'POST',
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      autoSubmitForm();
    })
    .catch(error => console.error('Error:', error));
}

function updateSelectFrame() {
  // Tạo biến kiểm tra giá trị chọn
  const selectedFrameValue = selectFrame.value;
  // Thông báo giá trị nhận
  console.log('Frame:', selectedFrameValue);
  var disableTextTop = document.getElementById("edit-top");
  var disableTextMiddle = document.getElementById("edit-middle");
  var disableTextBottom = document.getElementById("edit-bottom");

  switch (selectedFrameValue) {
    case 'what':
      disableTextTop.disabled = true;
      disableTextMiddle.disabled = true;
      disableTextMiddle.value = "";
      disableTextTop.value = "";
      break;
    case 'add':
    case 'surround':
      disableTextTop.disabled = false;
      disableTextMiddle.disabled = true;
      disableTextMiddle.value = "";
      break;
    default:
      disableTextTop.disabled = false;
      disableTextMiddle.disabled = false;
  }
}

dropArea.addEventListener("dragover", function (e) {
  e.preventDefault();
});

dropArea.addEventListener("drop", function (e) {
  e.preventDefault();
  inputFile.files = e.dataTransfer.files;
  uploadImage()
});


const setWatermarkPosition = document.getElementById("setWatermarkPosition")
// Hàm tự động gửi form, và giá trị của form
function autoSubmitForm() {
  // Lấy giá trị của form

  var formData = {
    top: document.getElementById("edit-top").value,
    middle: document.getElementById("edit-middle").value,
    bottom: document.getElementById("edit-bottom").value,
    frame: document.getElementById('edit-frame').value,
    watermark: textWatermark.value,
    watermarkFrame: selectedLayoutWatermark.value,
    watermarkPos: setWatermarkPosition.value
  }

  console.log("watermark: ", formData["watermark"]);
  // Nếu watermark có giá trị khác rỗng thì disable uploadWatermark
  if (formData["watermark"] == "") {
    // if (textWatermark.disabled = true)
    selectedLayoutWatermark.disabled = false;
    inputWatermark.disabled = false;
  }
  else {
    inputWatermark.value = null;
    inputWatermark.disabled = true;
    selectedLayoutWatermark.disabled = false;
  }

  if (inputWatermark.value == "" && formData["watermark"] == "") {
    selectedLayoutWatermark.disabled = true;
    setWatermarkPosition.disabled = true;
  }
  else {
    if (selectedLayoutWatermark.value == "conner")
      setWatermarkPosition.disabled = false;
    else
      setWatermarkPosition.disabled = true;
  }

  downloadButton.disabled = false;
  // Sử dụng Fetch API gửi tín hiệu lên server
  fetch('/update_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData),
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      const token = data.token;
      const imgElement = new Image();
      const randomParam = Math.random();
      imgElement.src = `static/images/exports/${nameImage}?random=${randomParam}&token=${token}`;
      console.log(imgElement.src);
      imgElement.onload = function () {
        imageView.style.backgroundImage = `url(${imgElement.src})`;
      };
      console.log(`url(static/images/exports/${nameImage})`);
    })
    .catch(error => console.error('Error:', error));
}