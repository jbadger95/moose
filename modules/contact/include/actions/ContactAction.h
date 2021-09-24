//* This file is part of the MOOSE framework
//* https://www.mooseframework.org
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html

#pragma once

#include "Action.h"
#include "MooseTypes.h"
#include "MooseEnum.h"

/// Enum used to select contact model type
enum class ContactModel
{
  FRICTIONLESS,
  GLUED,
  COULOMB,
};

/// Enum used to select contact formulation
enum class ContactFormulation
{
  RANFS,
  KINEMATIC,
  PENALTY,
  AUGMENTED_LAGRANGE,
  TANGENTIAL_PENALTY,
  MORTAR
};

/**
 * Action class for creating constraints, kernels, and user objects necessary for mechanical
 * contact.
 */

class ContactAction : public Action
{
public:
  static InputParameters validParams();

  ContactAction(const InputParameters & params);

  virtual void act() override;

  using Action::addRelationshipManagers;
  virtual void addRelationshipManagers(Moose::RelationshipManagerType input_rm_type) override;

  /**
   * Get contact model
   * @return enum
   */
  static MooseEnum getModelEnum();
  /**
   * Get mortar approach
   * @return enum
   */
  static MooseEnum getMortarApproach();
  /**
   * Get contact formulation
   * @return enum
   */
  static MooseEnum getFormulationEnum();
  /**
   * Get contact system
   * @return enum
   */
  static MooseEnum getSystemEnum();
  /**
   * Get smoothing type
   * @return enum
   */
  static MooseEnum getSmoothingEnum();
  /**
   * Define parameters used by multiple contact objects
   * @return InputParameters object populated with common parameters
   */
  static InputParameters commonParameters();

protected:
  /// Primary boundary names for mechanical contact
  const std::vector<BoundaryName> _primary;
  /// Secondary boundary names for mechanical contact
  const std::vector<BoundaryName> _secondary;
  /// Contact model type enum
  const MooseEnum _model;
  /// Contact formulation type enum
  const MooseEnum _formulation;
  /// Mesh generator name for Mortar contact formulation
  const MeshGeneratorName _mesh_gen_name;
  /// Mortar approach (weighted --variationally consistent-- or legacy)
  enum class MortarApproach
  {
    Weighted,
    Legacy
  };
  const MortarApproach _mortar_approach;
  /// Whether to use the dual Mortar approach
  bool _use_dual;
  /// Whether the user supplied lowerD blocks for mortar
  bool _has_lower_blocks;
  /// Number of contact pairs on which to enable mechanical contact
  const unsigned int _number_pairs;

private:
  /**
   * Generate mesh and other Moose objects for Mortar contact
   */
  void addMortarContact();
  /**
   * Generate constraints for node to face contact
   */
  void addNodeFaceContact();
};
