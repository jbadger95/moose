# Hertz Contact: Sphere on sphere

# Spheres have the same radius, Young's modulus, and Poisson's ratio.

# Define E:
# 1/E = (1-nu1^2)/E1 + (1-nu2^2)/E2
#
# Effective radius R:
# 1/R = 1/R1 + 1/R2
#
# F is the applied compressive load.
#
# Area of contact a::
# a^3 = 3FR/4E
#
# Depth of indentation d:
# d = a^2/R
#
#
# Let R1 = R2 = 2.  Then R = 1.
#
# Let nu1 = nu2 = 0.25, E1 = E2 = 1.40625e7.  Then E = 7.5e6.
#
# Let F = 10000.  Then a = 0.1, d = 0.01.
#

[GlobalParams]
  volumetric_locking_correction = false
  displacements = 'disp_x disp_y disp_z'
[]

[Mesh]
  [load]
    type = FileMeshGenerator
    file = hertz_contact.e
  []
  [secondary]
    input = load
    type = LowerDBlockFromSidesetGenerator
    sidesets = 100
    new_block_id = '102'
    new_block_name = 'secondary_lower'
  []
  [primary]
    input = secondary
    type = LowerDBlockFromSidesetGenerator
    sidesets = 1000
    new_block_id = '101'
    new_block_name = 'primary_lower'
  []
  # allow_renumbering = false
[] # Mesh

[Functions]
  [./pressure]
    type = PiecewiseLinear
    x = '0. 1. 2.'
    y = '0. 1. 1.'
    scale_factor = 795.77471545947674 # 10000/pi/2^2
  [../]
  [./disp_y]
    type = PiecewiseLinear
    x = '0.  1.    2.'
    y = '0. -0.01 -0.01'
  [../]
[] # Functions

[Variables]

  [./disp_x]
    # order = SECOND
    family = LAGRANGE
    block = '1 1000'
  [../]

  [./disp_y]
    # order = SECOND
    family = LAGRANGE
    block = '1 1000'
  [../]

  [./disp_z]
    # order = SECOND
    family = LAGRANGE
    block = '1 1000'
  [../]

  [./normal_lm]
    block = 'secondary_lower'
    # family = MONOMIAL
    # order = CONSTANT
    # use_dual = true
  [../]

[] # Variables

[AuxVariables]

  [./stress_xx]
    order = CONSTANT
    family = MONOMIAL
    block = '1 1000'
  [../]
  [./stress_yy]
    order = CONSTANT
    family = MONOMIAL
    block = '1 1000'
  [../]
  [./stress_zz]
    order = CONSTANT
    family = MONOMIAL
    block = '1 1000'
  [../]
  [./stress_xy]
    order = CONSTANT
    family = MONOMIAL
    block = '1 1000'
  [../]
  [./stress_yz]
    order = CONSTANT
    family = MONOMIAL
    block = '1 1000'
  [../]
  [./stress_zx]
    order = CONSTANT
    family = MONOMIAL
    block = '1 1000'
  [../]
  [./vonmises]
    order = CONSTANT
    family = MONOMIAL
    block = '1 1000'
  [../]
  [./hydrostatic]
    order = CONSTANT
    family = MONOMIAL
    block = '1 1000'
  [../]

[] # AuxVariables

[Modules/TensorMechanics/Master]
  [./all]
    add_variables = true
    strain = SMALL
    block = '1 1000'
  #  extra_vector_tags = 'ref'
  [../]
[]
[AuxKernels]

  [./stress_xx]
    type = RankTwoAux
    rank_two_tensor = stress
    index_i = 0
    index_j = 0
    variable = stress_xx
    block = '1 1000'
  [../]
  [./stress_yy]
    type = RankTwoAux
    rank_two_tensor = stress
    index_i = 1
    index_j = 1
    variable = stress_yy
    block = '1 1000'
  [../]
  [./stress_zz]
    type = RankTwoAux
    rank_two_tensor = stress
    index_i = 2
    index_j = 2
    variable = stress_zz
    block = '1 1000'
  [../]
  [./stress_xy]
    type = RankTwoAux
    rank_two_tensor = stress
    index_i = 0
    index_j = 1
    variable = stress_xy
    block = '1 1000'
  [../]
  [./stress_yz]
    type = RankTwoAux
    rank_two_tensor = stress
    index_i = 1
    index_j = 2
    variable = stress_yz
    block = '1 1000'
  [../]
  [./stress_zx]
    type = RankTwoAux
    rank_two_tensor = stress
    index_i = 2
    index_j = 0
    variable = stress_zx
    block = '1 1000'
  [../]
[] # AuxKernels

[BCs]

  [./base_x]
    type = DirichletBC
    variable = disp_x
    boundary = 1000
    value = 0.0
  [../]
  [./base_y]
    type = DirichletBC
    variable = disp_y
    boundary = 1000
    value = 0.0
  [../]
  [./base_z]
    type = DirichletBC
    variable = disp_z
    boundary = 1000
    value = 0.0
  [../]

  # [./symm_x]
  #   type = DirichletBC
  #   variable = disp_x
  #   boundary = 1
  #   value = 0.0
  # [../]
  # [./symm_z]
  #   type = DirichletBC
  #   variable = disp_z
  #   boundary = 3
  #   value = 0.0
  # [../]
  [./disp_y]
    type = FunctionDirichletBC
    variable = disp_y
    boundary = 2
    function = disp_y
  [../]

[] # BCs


[Constraints]
  [normal_lm]
    type = ComputeWeightedGapLMMechanicalContact
    primary_boundary = 1000
    secondary_boundary = 100
    primary_subdomain = 'primary_lower'
    secondary_subdomain = 'secondary_lower'
    variable = normal_lm
    disp_x = disp_x
    disp_y = disp_y
    disp_z = disp_z
    use_displaced_mesh = true
    give_me_wrong_results = false
    c = 1
  []
  [normal_x]
    type = NormalMortarMechanicalContact
    primary_boundary = 1000
    secondary_boundary = 100
    primary_subdomain = 'primary_lower'
    secondary_subdomain = 'secondary_lower'
    variable = normal_lm
    secondary_variable = disp_x
    component = x
    use_displaced_mesh = true
    compute_lm_residuals = false
  []
  [normal_y]
    type = NormalMortarMechanicalContact
    primary_boundary = 1000
    secondary_boundary = 100
    primary_subdomain = 'primary_lower'
    secondary_subdomain = 'secondary_lower'
    variable = normal_lm
    secondary_variable = disp_y
    component = y
    use_displaced_mesh = true
    compute_lm_residuals = false
  []
  [normal_z]
    type = NormalMortarMechanicalContact
    primary_boundary = 1000
    secondary_boundary = 100
    primary_subdomain = 'primary_lower'
    secondary_subdomain = 'secondary_lower'
    variable = normal_lm
    secondary_variable = disp_z
    component = z
    use_displaced_mesh = true
    compute_lm_residuals = false
  []
[]

# [Contact]
#   [./dummy_name]
#     mesh = load
#     primary = 1000
#     secondary = 100
#     formulation = mortar
#     mortar_approach = weighted
#     model = frictionless
#     # use_dual = true
#     c_normal = 1e7
#     # give_me_wrong_results = false
#   [../]
# []

[Materials]
  [./tensor]
    type = ComputeIsotropicElasticityTensor
    block = '1'
    youngs_modulus = 1.40625e4
    poissons_ratio = 0.25
  [../]
  [./stress]
    type = ComputeLinearElasticStress
    block = '1'
  [../]

  [./tensor_1000]
    type = ComputeIsotropicElasticityTensor
    block = '1000'
    youngs_modulus = 1e3
    poissons_ratio = 0.0
  [../]
  [./stress_1000]
    type = ComputeLinearElasticStress
    block = '1000'
  [../]

[] # Materials

[Preconditioning]
  [./SMP]
    type = SMP
    full = true
  []
[]

[Executioner]

  type = Transient

  solve_type = 'PJFNK'

  petsc_options_iname = '-pc_type -pc_factor_mat_solver_package'
  petsc_options_value = 'lu     superlu_dist'

  line_search = 'none'

  nl_abs_tol = 1e-7
  l_max_its = 30
  start_time = 0.0
  dt = 0.05
  end_time = 0.5 # was 2.0

  [./Quadrature]
    order = FIFTH
  [../]

[] # Executioner

# [Postprocessors]
#   [./maxdisp]
#     type = NodalVariableValue
#     nodeid = 386 # 387-1 where 387 is the exodus node number of the top-center node
#     variable = disp_y
#   [../]
# []

[Debug]
  show_var_residual_norms = true
[]

[Outputs]
  [./out]
    type = Exodus
    # elemental_as_nodal = true
  [../]
[] # Outputs
