const mongoose = require("mongoose");
const coursesList = require("../courses.json");
let mongohost = process.env.MONGODB_HOST || "localhost"
let mongoport = process.env.MONGODB_PORT || 27017
let dbname = process.env.MONGODB_NAME || "kimo"
let mongourl = `mongodb://${mongohost}:${mongoport}/${dbname}`
console.log(mongourl)
mongoose.connect(mongourl)
const db = mongoose.connection ; 

db.on("error",()=> {
    console.log("error in connecting to mongodb ")
})
db.on("connected",async () => {
    console.log("mongodb connected ")
    const Chapters = new mongoose.Schema({
        name: String,
        text: String,
        like_count: {
            type: Number ,
            default: 0 
        },
        dislike_count: {
            type: Number ,
            default: 0 ,
        }
    })
    const Domains = new mongoose.Schema({
        domain: String
    })
    const Courses = new mongoose.Schema({
        name: {
            type: String ,
            required: true 
        },
        date: {
            type: Date,
            required: true 
        },
        description: {
            type: String,
            required: true ,
            max: 400
        },
        domains: [mongoose.Types.ObjectId],
        chapters: [Chapters],
        total_like: Number,
        total_dislike: Number,
    })
    const CourseModel = db.model("course",Courses);
    const DomainModel = db.model("domain",Domains);

    DomainModel.createCollection()
    CourseModel.createCollection();
    await Courses.index({  domains: 1, name: 1});// follow esr rule.
    await Courses.index({   domains: 1 , date : -1})
    await Courses.index({"chapters._id": 1})
    await Courses.index({name: 1})
    await Courses.index({date: -1})
    
    for(let i = 0 ; i < coursesList.length ; i++) {
        let course = coursesList[i];
        // Check for a domain if exists get its id otherwise create one in db .
        let domainsList = []
        for(let j = 0 ; j < coursesList[i].domain.length; j++){
            let domainCreateIfDoesntExist = await DomainModel.findOneAndUpdate({domain: coursesList[i].domain[j]},{},{upsert: true , new: true });
            if(domainCreateIfDoesntExist){
                domainsList.push(domainCreateIfDoesntExist._id);
            }
        }
        let chaptersList = coursesList[i].chapters.map((chapter)=> {
            return {
                name: chapter.name,
                text: chapter.text,
                dislike_count: 0,
                like_count: 0
            }
        })
        let data = await db.model("course").findOneAndUpdate(
            {name: course.name},
            {
                $set: {
                    date: course.date,
                    description: course.description,
                    total_like: 0,
                    total_dislike: 0,
                },
                $addToSet: {
                    domains: { $each : domainsList},
                    chapters: { $each : chaptersList}
                }
            },
            {upsert: true, new: true});

        console.log(data);
    }
    db.close()
});


