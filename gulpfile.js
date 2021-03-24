var babel = require('gulp-babel'),
    browserify = require('browserify'),
    source = require('vinyl-source-stream'),
    buffer = require('vinyl-buffer'),
    rename = require('gulp-rename'),
    uglify = require('gulp-uglify'),
    gulp = require('gulp')
    del = require('del');

gulp.task('clean-temp', function(){
  return del(['dest']);
});

gulp.task('es6-commonjs', gulp.series(['clean-temp'], function(){
  return gulp.src(['node_modules/@amcharts/*.js','node_modules/@amcharts/**/*.js'])
    // .pipe(babel())
    .pipe(babel({
	  presets:["env"]
	}))
    .pipe(gulp.dest('dest/temp'));
}));

gulp.task('es6-commonjs-2', function(){
  return gulp.src(['node_modules/@amcharts/amcharts4/.internal/*.js','node_modules/@amcharts/amcharts4/.internal/**/*.js'])
    // .pipe(babel())
    .pipe(babel({
	  presets:["env"]
	}))
    .pipe(gulp.dest('dest/temp'));
});

gulp.task('es6-commonjs-3', function(){
  return gulp.src(['dest/temp/amcharts4/export_old.js'])
    // .pipe(babel())
    .pipe(babel({
	  presets:["env"]
	}))
    .pipe(gulp.dest('dest/temp/amcharts4/export2.js'));
});

gulp.task('bundle-commonjs-clean', function(){
  return del(['es5/commonjs']);
});

gulp.task('commonjs-bundle',  gulp.series(['bundle-commonjs-clean','es6-commonjs'], function(){
  return browserify(['dest/temp/bootstrap.js']).bundle()
    .pipe(source('amcharts4.js'))
    .pipe(buffer())
    .pipe(uglify())
    .pipe(rename('amcharts4.js'))
    .pipe(gulp.dest("es5/commonjs"));
}));

gulp.task('commonjs-bundle-straight', function(){
  return browserify(['dest/temp/amcharts4/core.js', 'dest/temp/amcharts4/charts.js', 'dest/temp/amcharts4/plugins/timeline.js', 'dest/temp/amcharts4/plugins/bullets.js', 'dest/temp/amcharts4/themes/animated.js', 'dest/temp/amcharts4/export.js']).bundle()
    .pipe(source('amcharts4.js'))
    .pipe(buffer())
    .pipe(uglify())
    .pipe(rename('amcharts4.js'))
    .pipe(gulp.dest("es5/commonjs"));
});

gulp.task('commonjs-bundle-straight2', function(){
  return browserify(['dest/temp/amcharts4/export.js']).bundle()
    .pipe(source('amcharts4.js'))
    .pipe(buffer())
    .pipe(uglify())
    .pipe(rename('amcharts4.js'))
    .pipe(gulp.dest("es5/commonjs"));
});


gulp.task('commonjs-bundle-straight3', function(){
  return browserify(['amcharts_4.10.17/core.js', 'amcharts_4.10.17/charts.js', 'amcharts_4.10.17/plugins/timeline.js', 'amcharts_4.10.17/plugins/bullets', 'amcharts_4.10.17/themes/animated.js']).bundle()
    .pipe(source('amcharts4.js'))
    .pipe(buffer())
    .pipe(uglify())
    .pipe(rename('amcharts4.js'))
    .pipe(gulp.dest("es5/commonjs"));
});

gulp.task('commonjs', gulp.series(['commonjs-bundle']));