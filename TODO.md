## Build goals
- [ ] Create auto clavicle for arm in build
- [ ] Write hand build with multiFk part
- [ ] Add some follow relationships


## Stretch goals
- [ ] Create layout rig
- [ ] Create deform rig
- [ ] Create rig interface API
- [ ] Add more readmes


## Current issues
- [x] Expose smarter get_control() at part level
- [x] Expose per control grp offset functionality before build time
- [ ] Expose per control shape offset functionality after build time


## File handling
- [ ] Consider a versioning system for data files
- [x] Write a settings data sub class to handle settings at part level


## Fundamental
- [ ] Tidy module creation
- [x] Split part creation so multi-parts can be made easier
- [x] Write test create methods for parts
- [ ] Write secondary (deformer) part logic
- [x] Add settings node
- [ ] Get config working
- [x] Write data I/O logic
- [ ] Refactor I/O logic to be a bit less automated
- [ ] Incorporate eval() methods for I/O data
- [ ] Write deformer save/load data logic


## Parts
- [x] Connect IkFk control shape vis
- [ ] Add settings attr to settings node, hidden to determine its a settings node
- [ ] Look into determining on describing which methods can be run pre or post create
- [x] Add IkFk stretch
- [x] Fix IkFkSpline
- [ ] Add detail to IkSpline for number of controls, clusters, etc
- [x] Write Fk part
- [x] Write FkChain part
- [x] Add Fk stretch logic
- [x] Write Ik part
- [x] Write Ik stretch
- [x] Add settings to proxy component
- [x] Add settings to skeleton component
- [x] Write IkFkChain part
- [x] Expose orient and point offsets to parts at creation time
- [x] Store control creation order to know first, last, etc
- [x] Add settings group
- [ ] Write a twist deformer part
- [x] Write a global part (named Base case global is reserved)
- [x] Write spine part
- [x] Write foot part
- [ ] Write multi part (combine parts?)
- [ ] Create face part library
- [ ] Write eye part
- [ ] Write mouth part
- [x] Write simple control part
- [ ] Create global control style to not be big quad arrow
- [ ] Aim polevector of IkRp at center of chain


## Utils
- [x] Write attribute library (properly)
- [ ] Tidy up name 
- [ ] Tidy up attr
- [x] Add vector utils
- [x] Add joint utils for easy joint creation for test methods
