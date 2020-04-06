$(document).ready(function(){
    // set up navigation bar
    $("#navlink-home").attr("href", "#")
        .html("Home");
    $("#navlink-quizset").attr("href", "quizset.html")
        .html("Quiz Sets");
    $("#navlink-results").attr("href", "#")
        .html("Results");
    $("#navlink-admin-edit").attr("href", "#")
        .html("Admin Edit");
    $("#navlink-admin-assess").attr("href", "#")
        .html("Admin Assess");
    
    // disable locked quizzes
    $("#quizset-inter").addClass("quizset-disable");
    $("#quizset-inter a").addClass("link-disable")
        .removeAttr("href");
    $("#quizset-adv").addClass("quizset-disable");
    $("#quizset-adv a").addClass("link-disable")
        .removeAttr("href");

    // set up footer
    $("#authorship").html("Created by Alan and Guohuan for CITS3403 Project 2");
});
