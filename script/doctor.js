$(document).ready(function () {
	for (let sp of _medicalSpecialties) {
		console.log(sp);
		$("#appointment_attentionArea").append($("<option>").val(sp).text(sp));
	}

	const database = firebase.database();

	const doctorsDB = database.ref("doctors");

	let doctorData;

	doctorsDB.on("value", (snapshot) => {
		doctorData = snapshot.val();
	});

	$("#appointment_attentionArea").on("change", function () {
		let value = this.value;
		
		$("#appointment_doctor > option:not(:first)").remove();

		Object.values(doctorData).forEach((elem) => {
			if(elem.specialty  === value){
				$("#appointment_doctor").append(
					$("<option>").val(elem.doctorId).text(elem.fullName)
				);
			}
		});
	});
});

(function main() {})();
