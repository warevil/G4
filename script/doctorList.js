$(document).ready(function () {
	console.log('Login Document');
	const database = firebase.database();

	const doctorsDB = database.ref("doctors");


	doctorsDB.on("value", (snapshot) => {
		doctorData = snapshot.val();

		console.log($(".doctorsList"));
		Object.values(doctorData).forEach((elem) => {
			console.log(elem);
			$("#doctorsList").append(
				`
				<div class="col-lg-3 col-md-6 d-flex mb-sm-4">
					<div class="staff">
						<div class="img mb-4" style="background-image: url('${elem.picture}');"></div>
						<div class="info text-center">
							<h3><a href="teacher-single.html">${elem.fullName}</a></h3>
							<span class="position">${elem.specialty}</span>
						</div>
					</div>
				</div>
				`
			);
		});
	});

		

});



